#!/usr/bin/env python3
"""
Test script for multi-provider search functionality.
Run this to verify your search API keys are working.
"""
import asyncio
import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.core.agent_tools import search_web
from app.core.config import settings


async def test_search():
    """Test the multi-provider search with a sample query."""
    
    print("=" * 80)
    print("🔍 Testing Multi-Provider Search API")
    print("=" * 80)
    
    # Check which APIs are configured
    print("\n📋 Configured Search Providers:")
    print(f"   Tavily:  {'✅ Configured' if settings.TAVILY_API_KEY else '❌ Not configured'}")
    print(f"   Serper:  {'✅ Configured' if settings.SERPER_API_KEY else '❌ Not configured'}")
    print(f"   DuckDuckGo: ✅ Always available (fallback)")
    
    if not settings.TAVILY_API_KEY and not settings.SERPER_API_KEY:
        print("\n⚠️  WARNING: No premium search APIs configured!")
        print("   Add API keys to backend/.env to improve search quality:")
        print("   - TAVILY_API_KEY=tvly-... (Get free key at https://tavily.com)")
        print("   - SERPER_API_KEY=... (Get free key at https://serper.dev)")
        print("\n   Falling back to DuckDuckGo (free but rate-limited)...")
    
    # Test query
    test_query = "HDFC Regalia credit card rewards rate"
    
    print(f"\n🔎 Testing search with query: '{test_query}'")
    print("-" * 80)
    
    try:
        result = await search_web.ainvoke({"query": test_query})
        
        print("\n✅ Search Result:")
        print("-" * 80)
        print(result)
        print("-" * 80)
        
        # Check which provider was used
        if "[Source: Tavily" in result:
            print("\n🎯 Provider Used: Tavily AI Search (Premium)")
        elif "[Source: Serper" in result:
            print("\n🎯 Provider Used: Serper/Google Search (Premium)")
        elif "[Source: DuckDuckGo" in result:
            print("\n🎯 Provider Used: DuckDuckGo (Free Fallback)")
        else:
            print("\n❌ Search failed - check error message above")
        
        print("\n" + "=" * 80)
        print("✅ Search test completed!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Error during search: {e}")
        print("\nTroubleshooting:")
        print("1. Check your API keys in backend/.env")
        print("2. Verify internet connection")
        print("3. Check API rate limits")


if __name__ == "__main__":
    asyncio.run(test_search())
