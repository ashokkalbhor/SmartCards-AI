"""
Simple cache manager for in-memory caching
"""

import hashlib
import time
from typing import Any, Optional, Dict
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class CacheManager:
    def __init__(self):
        self.cache = {}
        self.max_size = 1000  # Maximum number of cache entries
    
    def _generate_key(self, prefix: str, content: str) -> str:
        """Generate cache key with prefix"""
        content_hash = hashlib.md5(content.encode()).hexdigest()
        return f"{prefix}:{content_hash}"
    
    async def get(self, key: str) -> Optional[Any]:
        """Get cached value"""
        try:
            if key in self.cache:
                entry = self.cache[key]
                if entry["expires_at"] > datetime.now():
                    return entry["value"]
                else:
                    # Remove expired entry
                    del self.cache[key]
            return None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None
    
    async def set(self, key: str, value: Any, ttl: int = 3600):
        """Set cached value with TTL in seconds"""
        try:
            # Remove oldest entries if cache is full
            if len(self.cache) >= self.max_size:
                self._cleanup_oldest()
            
            expires_at = datetime.now() + timedelta(seconds=ttl)
            self.cache[key] = {
                "value": value,
                "expires_at": expires_at,
                "created_at": datetime.now()
            }
        except Exception as e:
            logger.error(f"Cache set error: {e}")
    
    async def get_or_set(self, key: str, default_func, ttl: int = 3600):
        """Get cached value or set default"""
        cached = await self.get(key)
        if cached is not None:
            return cached
        
        value = await default_func()
        await self.set(key, value, ttl)
        return value
    
    def _cleanup_oldest(self):
        """Remove oldest cache entries"""
        if not self.cache:
            return
        
        # Sort by creation time and remove oldest 10%
        sorted_entries = sorted(
            self.cache.items(), 
            key=lambda x: x[1]["created_at"]
        )
        
        to_remove = len(sorted_entries) // 10  # Remove 10%
        for i in range(to_remove):
            key = sorted_entries[i][0]
            del self.cache[key]
    
    def clear(self):
        """Clear all cache entries"""
        self.cache.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        now = datetime.now()
        active_entries = 0
        expired_entries = 0
        
        for entry in self.cache.values():
            if entry["expires_at"] > now:
                active_entries += 1
            else:
                expired_entries += 1
        
        return {
            "total_entries": len(self.cache),
            "active_entries": active_entries,
            "expired_entries": expired_entries,
            "max_size": self.max_size
        } 