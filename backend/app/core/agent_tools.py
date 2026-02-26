import logging
import asyncio
from typing import Optional, List, Dict, Any
import json
from io import BytesIO

from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

# PDF and Browser libraries
import pdfplumber
import aiohttp
from playwright.async_api import async_playwright

from app.core.config import settings

logger = logging.getLogger(__name__)

# --- Tool 1: Multi-Provider Robust Search ---
@tool
async def search_web(query: str) -> str:
    """
    Robust web search with automatic fallback across multiple providers.
    Tries: Tavily → Serper → DuckDuckGo.
    Returns a string summary of results from the first successful provider.
    """
    logger.info(f"Starting multi-provider search for: {query}")
    
    # Try Tavily first (best for AI, 1000 free searches/month)
    if settings.TAVILY_API_KEY:
        try:
            logger.info("Attempting search with Tavily...")
            from tavily import TavilyClient
            
            tavily_client = TavilyClient(api_key=settings.TAVILY_API_KEY)
            response = tavily_client.search(
                query=query,
                search_depth="basic",  # "basic" or "advanced"
                max_results=5
            )
            
            if response and response.get('results'):
                results = response['results']
                summary = "[Source: Tavily AI Search]\n\n"
                for r in results:
                    summary += f"Title: {r.get('title', 'N/A')}\n"
                    summary += f"URL: {r.get('url', 'N/A')}\n"
                    summary += f"Content: {r.get('content', 'N/A')}\n"
                    if r.get('score'):
                        summary += f"Relevance Score: {r.get('score')}\n"
                    summary += "\n"
                logger.info("Tavily search successful")
                return summary
        except Exception as e:
            logger.warning(f"Tavily search failed: {e}")
    
    # Try Serper (Google quality, 2500 free searches/month)
    if settings.SERPER_API_KEY:
        try:
            logger.info("Attempting search with Serper (Google)...")
            import requests
            
            url = "https://google.serper.dev/search"
            payload = json.dumps({"q": query, "num": 5})
            headers = {
                'X-API-KEY': settings.SERPER_API_KEY,
                'Content-Type': 'application/json'
            }
            
            response = requests.post(url, headers=headers, data=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                summary = "[Source: Serper/Google Search]\n\n"
                
                # Extract organic results
                if data.get('organic'):
                    for r in data['organic'][:5]:
                        summary += f"Title: {r.get('title', 'N/A')}\n"
                        summary += f"URL: {r.get('link', 'N/A')}\n"
                        summary += f"Snippet: {r.get('snippet', 'N/A')}\n\n"
                    logger.info("Serper search successful")
                    return summary
        except Exception as e:
            logger.warning(f"Serper search failed: {e}")
    
    # Fallback to DuckDuckGo (free, unlimited but rate-limited)
    try:
        logger.info("Attempting search with DuckDuckGo (fallback)...")
        from duckduckgo_search import DDGS
        
        # Add small delay to avoid rate limiting
        await asyncio.sleep(1)
        
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5, backend="lite"))
            
            if results:
                summary = "[Source: DuckDuckGo]\n\n"
                for r in results:
                    summary += f"Title: {r['title']}\n"
                    summary += f"URL: {r['href']}\n"
                    summary += f"Snippet: {r['body']}\n\n"
                logger.info("DuckDuckGo search successful")
                return summary
    except Exception as e:
        logger.error(f"DuckDuckGo search failed: {e}")
    
    # All providers failed
    error_msg = "Error: All search providers failed. "
    if not settings.TAVILY_API_KEY and not settings.SERPER_API_KEY:
        error_msg += "Please configure at least one search API key (TAVILY_API_KEY or SERPER_API_KEY) in your .env file."
    else:
        error_msg += "Please check your API keys and network connection."
    
    logger.error(error_msg)
    return error_msg

# --- Tool 2: Browser Scraper (Playwright) ---
@tool
async def scrape_web_page(url: str) -> str:
    """
    Scrape a webpage using a headless browser (Playwright).
    Handles JavaScript rendering and basic anti-bot evasions.
    Returns the text content of the page.
    """
    logger.info(f"Scraping URL with Playwright: {url}")
    
    # Basic validation
    if not url or not (url.startswith('http://') or url.startswith('https://')):
        return "Error: Invalid URL provided."
        
    playwright = None
    browser = None
    try:
        playwright = await async_playwright().start()
        
        # Launch browser with stealthier args
        browser = await playwright.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-setuid-sandbox'
            ]
        )
        
        # Create context with realistic user agent
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            viewport={'width': 1280, 'height': 800}
        )
        
        page = await context.new_page()
        
        # Navigate with timeout
        await page.goto(url, timeout=60000, wait_until='domcontentloaded')
        
        # Extract text - prefer innerText for readability
        # We also strip excessive whitespace
        content = await page.evaluate("() => document.body.innerText")
        
        # Basic cleaning
        cleaned_content = "\n".join(
            [line.strip() for line in content.split('\n') if line.strip()]
        )
        
        return cleaned_content[:50000] # Limit response size
        
    except Exception as e:
        logger.error(f"Playwright scraping failed for {url}: {e}")
        return f"Error scraping page: {str(e)}"
    finally:
        if browser:
            await browser.close()
        if playwright:
            await playwright.stop()

# --- Tool 3: PDF Parser ---
@tool
async def parse_pdf(url: str) -> str:
    """
    Download and parse a PDF file from a URL.
    Extracts both text and tables (formatted as Markdown).
    Useful for analyzing Terms and Conditions documents.
    """
    logger.info(f"Parsing PDF from URL: {url}")
    
    try:
        # Download the PDF first
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return f"Error: Failed to download PDF. Status code: {response.status}"
                data = await response.read()
        
        # Parse with pdfplumber
        final_text = []
        
        with pdfplumber.open(BytesIO(data)) as pdf:
            for i, page in enumerate(pdf.pages):
                # 1. Extract Text
                text = page.extract_text() or ""
                
                # 2. Extract Tables
                tables = page.extract_tables()
                table_text = ""
                if tables:
                    table_text = "\n[Detected Tables]:\n"
                    for table in tables:
                        # Convert table to markdown-like format
                        # Filter out None values
                        clean_table = [[str(cell or "").replace("\n", " ").strip() for cell in row] for row in table]
                        
                        # Calculate column widths (simple approach) 
                        # This is just for readable plain text output
                        if clean_table:
                            # Create a simple representation
                            for row in clean_table:
                                table_text += " | ".join(row) + "\n"
                            table_text += "\n"
                
                page_content = f"--- Page {i+1} ---\n{text}\n{table_text}"
                final_text.append(page_content)
                
        return "\n".join(final_text)[:50000] # Limit size
        
    except Exception as e:
        logger.error(f"PDF parsing failed for {url}: {e}")
        return f"Error parsing PDF: {str(e)}"
