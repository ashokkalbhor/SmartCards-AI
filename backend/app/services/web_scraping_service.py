"""
Web Scraping Service - Fetch card data from official bank websites
"""
import logging
import asyncio
from typing import Optional, Dict, Any
from urllib.parse import urlparse
import aiohttp
from aiohttp import http_exceptions
from bs4 import BeautifulSoup
from io import BytesIO
import pdfplumber
import requests

logger = logging.getLogger(__name__)


class WebScrapingService:
    """Service for fetching and preprocessing web content from bank sites"""
    
    def __init__(self):
        self.timeout = aiohttp.ClientTimeout(total=30)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    async def fetch_page_content(self, url: str) -> Optional[str]:
        """Fetch and clean HTML content from a URL"""
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        content_type = response.headers.get('Content-Type', '').lower()
                        if 'pdf' in content_type:
                            data = await response.read()
                            return self._extract_pdf_text(data)
                        else:
                            try:
                                html = await response.text()
                            except UnicodeDecodeError:
                                raw = await response.read()
                                html = raw.decode('utf-8', errors='ignore')
                            return self._clean_html(html)
                    else:
                        logger.error(f"Failed to fetch {url}: HTTP {response.status}")
                        return None
        except asyncio.TimeoutError:
            logger.error(f"Timeout fetching {url}")
            return None
        except http_exceptions.LineTooLong:
            logger.warning(f"Header too long for {url}, retrying with requests")
            return await asyncio.to_thread(self._fetch_with_requests, url)
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def _fetch_with_requests(self, url: str) -> Optional[str]:
        """Synchronous fallback using requests for servers with large headers."""
        try:
            timeout = self.timeout.total or 30
            response = requests.get(url, headers=self.headers, timeout=timeout)
            if response.status_code != 200:
                logger.error(f"Requests fallback failed for {url}: HTTP {response.status_code}")
                return None

            content_type = response.headers.get('Content-Type', '').lower()
            if 'pdf' in content_type:
                return self._extract_pdf_text(response.content)

            response.encoding = response.encoding or 'utf-8'
            return self._clean_html(response.text)
        except requests.exceptions.Timeout:
            logger.error(f"Requests fallback timed out for {url}")
        except Exception as exc:
            logger.error(f"Requests fallback error for {url}: {exc}")
        return None
    
    def _clean_html(self, html: str) -> str:
        """Clean and extract readable text from HTML"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            return text
        except Exception as e:
            logger.error(f"Error cleaning HTML: {e}")
            return html

    def _extract_pdf_text(self, data: bytes) -> Optional[str]:
        """Extract text from PDF bytes."""
        try:
            buffer = BytesIO(data)
            with pdfplumber.open(buffer) as pdf:
                texts = []
                for page in pdf.pages:
                    texts.append(page.extract_text() or "")
            combined = "\n".join(texts).strip()
            if not combined:
                logger.warning("PDF extracted but contained no text")
            return combined or None
        except Exception as e:
            logger.error(f"Failed to extract PDF text: {e}")
            return None
    
    def is_trusted_bank_url(self, url: str) -> bool:
        """Verify if URL is from a trusted bank domain"""
        trusted_domains = [
            'hdfcbank.com',
            'icicibank.com',
            'sbi.co.in',
            'axisbank.com',
            'kotakbank.com',
            'yesbank.in',
            'indusind.com',
            'rbl.com',
            'rblbank.com',
            'idbi.com',
            'pnbindia.in',
            'bankofbaroda.in',
            'canarabank.com',
            'unionbankofindia.co.in',
            'indianbank.in',
            'sc.com/in',  # Standard Chartered
            'citibank.co.in',
            'hsbc.co.in',
            'americanexpress.com',
        ]
        
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            
            # Remove www. prefix
            if domain.startswith('www.'):
                domain = domain[4:]
            
            return any(domain.endswith(trusted) for trusted in trusted_domains)
        except Exception as e:
            logger.error(f"Error validating URL {url}: {e}")
            return False
    
    async def fetch_multiple_pages(self, urls: list) -> Dict[str, str]:
        """Fetch content from multiple URLs concurrently"""
        tasks = [self.fetch_page_content(url) for url in urls if self.is_trusted_bank_url(url)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        content_map = {}
        for url, result in zip(urls, results):
            if isinstance(result, Exception):
                logger.error(f"Error fetching {url}: {result}")
                content_map[url] = None
            else:
                content_map[url] = result
        
        return content_map
    
    def chunk_content(self, content: str, max_tokens: int = 100000) -> list:
        """Chunk large content into smaller pieces for processing"""
        # Rough estimate: 1 token ≈ 4 characters
        max_chars = max_tokens * 4
        
        if len(content) <= max_chars:
            return [content]
        
        # Split by sections/paragraphs
        chunks = []
        current_chunk = []
        current_length = 0
        
        for paragraph in content.split('\n\n'):
            para_length = len(paragraph)
            
            if current_length + para_length > max_chars and current_chunk:
                chunks.append('\n\n'.join(current_chunk))
                current_chunk = [paragraph]
                current_length = para_length
            else:
                current_chunk.append(paragraph)
                current_length += para_length
        
        if current_chunk:
            chunks.append('\n\n'.join(current_chunk))
        
        return chunks
