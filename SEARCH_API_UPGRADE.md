# 🔍 Search API Upgrade Guide

## Current Problem
Your internet search APIs are not responding reliably:
- DuckDuckGo search gets rate-limited/blocked
- OpenAI's `web_search` tool has compatibility issues
- No fallback search providers

## Solutions (Choose One or Combine)

### ✅ **Option 1: Tavily API (RECOMMENDED)**
**Best for**: Production-grade search with AI-optimized results

#### 1. Install Tavily
```bash
cd /Users/ashokkumarkalbhor/SmartCards-AI/backend
pip install tavily-python
```

#### 2. Get API Key
- Go to https://tavily.com
- Sign up (Free tier: 1000 searches/month)
- Get your API key

#### 3. Add to `.env`
```bash
TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxxxxxxx
```

#### 4. Update `agent_tools.py`
Replace the `search_web` tool with:

```python
from langchain_community.tools.tavily_search import TavilySearchResults

@tool
def search_web_tavily(query: str) -> str:
    """
    Search the web using Tavily API (AI-optimized search).
    Returns detailed, relevant results from authoritative sources.
    """
    try:
        tavily_search = TavilySearchResults(
            max_results=5,
            search_depth="advanced",  # or "basic" for faster
            include_answer=True,
            include_raw_content=False
        )
        results = tavily_search.invoke({"query": query})
        
        if not results:
            return "No results found."
        
        summary = ""
        for r in results:
            summary += f"Title: {r['title']}\n"
            summary += f"URL: {r['url']}\n"
            summary += f"Content: {r['content']}\n"
            if 'answer' in r:
                summary += f"AI Summary: {r['answer']}\n"
            summary += "\n"
        return summary
    except Exception as e:
        logger.error(f"Tavily search failed: {e}")
        return f"Error performing search: {str(e)}"
```

---

### ✅ **Option 2: Serper API (Google Search)**
**Best for**: Google-quality search results

#### 1. Install
```bash
pip install google-search-results
```

#### 2. Get API Key
- Go to https://serper.dev
- Sign up (Free tier: 2500 searches/month)
- Get your API key

#### 3. Add to `.env`
```bash
SERPER_API_KEY=xxxxxxxxxxxxxxxxxxxxx
```

#### 4. Add to `agent_tools.py`
```python
from langchain_community.utilities import GoogleSerperAPIWrapper

@tool
def search_web_serper(query: str) -> str:
    """
    Search using Google via Serper API.
    Returns high-quality Google search results.
    """
    try:
        search = GoogleSerperAPIWrapper()
        results = search.run(query)
        return results
    except Exception as e:
        logger.error(f"Serper search failed: {e}")
        return f"Error performing search: {str(e)}"
```

---

### ✅ **Option 3: Brave Search API**
**Best for**: Privacy-focused, reliable search

#### 1. Install
```bash
pip install langchain-community
```

#### 2. Get API Key
- Go to https://brave.com/search/api/
- Sign up (Free tier: 2000 searches/month)
- Get your API key

#### 3. Add to `.env`
```bash
BRAVE_SEARCH_API_KEY=xxxxxxxxxxxxxxxxxxxxx
```

#### 4. Add to `agent_tools.py`
```python
from langchain_community.tools import BraveSearch

@tool
def search_web_brave(query: str) -> str:
    """
    Search using Brave Search API.
    Privacy-focused, reliable search results.
    """
    try:
        search = BraveSearch.from_api_key(
            api_key=settings.BRAVE_SEARCH_API_KEY,
            search_kwargs={"count": 5}
        )
        results = search.run(query)
        return results
    except Exception as e:
        logger.error(f"Brave search failed: {e}")
        return f"Error performing search: {str(e)}"
```

---

### ✅ **Option 4: Multi-Provider Fallback (BEST APPROACH)**
Combine multiple search providers with automatic fallback:

```python
@tool
async def search_web_robust(query: str) -> str:
    """
    Robust web search with automatic fallback across multiple providers.
    Tries: Tavily → Serper → Brave → DuckDuckGo
    """
    # Try Tavily first (best for AI)
    if settings.TAVILY_API_KEY:
        try:
            from langchain_community.tools.tavily_search import TavilySearchResults
            tavily = TavilySearchResults(max_results=5)
            results = tavily.invoke({"query": query})
            if results:
                return _format_results(results, "Tavily")
        except Exception as e:
            logger.warning(f"Tavily failed: {e}")
    
    # Try Serper (Google quality)
    if settings.SERPER_API_KEY:
        try:
            from langchain_community.utilities import GoogleSerperAPIWrapper
            search = GoogleSerperAPIWrapper()
            results = search.run(query)
            if results:
                return f"[Source: Serper/Google]\n{results}"
        except Exception as e:
            logger.warning(f"Serper failed: {e}")
    
    # Try Brave (privacy-focused)
    if settings.BRAVE_SEARCH_API_KEY:
        try:
            from langchain_community.tools import BraveSearch
            search = BraveSearch.from_api_key(api_key=settings.BRAVE_SEARCH_API_KEY)
            results = search.run(query)
            if results:
                return f"[Source: Brave]\n{results}"
        except Exception as e:
            logger.warning(f"Brave failed: {e}")
    
    # Fallback to DuckDuckGo (free, but rate-limited)
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5, backend="html"))
            if results:
                summary = "[Source: DuckDuckGo]\n"
                for r in results:
                    summary += f"Title: {r['title']}\nURL: {r['href']}\nSnippet: {r['body']}\n\n"
                return summary
    except Exception as e:
        logger.error(f"All search providers failed. Last error: {e}")
    
    return "Error: All search providers unavailable. Please check API keys."

def _format_results(results: list, source: str) -> str:
    """Helper to format search results consistently."""
    summary = f"[Source: {source}]\n"
    for r in results:
        summary += f"Title: {r.get('title', 'N/A')}\n"
        summary += f"URL: {r.get('url', r.get('href', 'N/A'))}\n"
        summary += f"Content: {r.get('content', r.get('body', 'N/A'))}\n\n"
    return summary
```

---

## 🔧 Configuration Updates

### 1. Update `backend/app/core/config.py`
```python
# Search API Keys
TAVILY_API_KEY: Optional[str] = None
SERPER_API_KEY: Optional[str] = None
BRAVE_SEARCH_API_KEY: Optional[str] = None
```

### 2. Update `backend/.env`
```bash
# Search APIs (add at least one)
TAVILY_API_KEY=tvly-xxxxx
# SERPER_API_KEY=xxxxx
# BRAVE_SEARCH_API_KEY=xxxxx
```

### 3. Update `requirements.txt`
```
tavily-python==0.3.3
google-search-results==2.4.2
```

---

## 🚀 Implementation Priority

1. **Immediate**: Add Tavily (best AI search, generous free tier)
2. **Backup**: Add Serper (Google quality)
3. **Long-term**: Implement multi-provider fallback system

---

## 📊 API Comparison

| Provider | Free Tier | Quality | Speed | AI-Optimized | Reliability |
|----------|-----------|---------|-------|--------------|-------------|
| **Tavily** | 1000/mo | ⭐⭐⭐⭐⭐ | Fast | ✅ Yes | ⭐⭐⭐⭐⭐ |
| **Serper** | 2500/mo | ⭐⭐⭐⭐⭐ | Fast | ❌ No | ⭐⭐⭐⭐⭐ |
| **Brave** | 2000/mo | ⭐⭐⭐⭐ | Fast | ❌ No | ⭐⭐⭐⭐ |
| **DuckDuckGo** | Unlimited | ⭐⭐⭐ | Slow | ❌ No | ⭐⭐ |

---

## ✅ Testing

After implementation, test with:

```python
from app.core.agent_tools import search_web_robust

# Test search
result = await search_web_robust("HDFC Regalia credit card rewards on Amazon")
print(result)
```

---

## 🎯 Recommendation

**Use Option 4 (Multi-Provider Fallback)** with:
1. **Primary**: Tavily (best for AI agents)
2. **Secondary**: Serper (Google quality)
3. **Tertiary**: DuckDuckGo (free fallback)

This gives you:
- ✅ 3500+ free searches per month
- ✅ Automatic failover
- ✅ AI-optimized results
- ✅ Production reliability
