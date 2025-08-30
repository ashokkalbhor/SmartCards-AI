import asyncio
import logging
import time
from typing import Optional, Any, Dict
from datetime import datetime, timedelta
import json
import hashlib

from app.core.config import settings

logger = logging.getLogger(__name__)


class CacheService:
    """In-memory cache service with TTL and retry logic"""
    
    def __init__(self):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.max_size = settings.CACHE_MAX_SIZE
        self.enabled = settings.CACHE_ENABLED
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.enabled:
            return None
        
        try:
            if key in self.cache:
                cache_entry = self.cache[key]
                
                # Check if expired
                if self._is_expired(cache_entry):
                    del self.cache[key]
                    return None
                
                # Update access time
                cache_entry["last_accessed"] = time.time()
                return cache_entry["value"]
            
            return None
            
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None
    
    async def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """Set value in cache with TTL"""
        if not self.enabled:
            return False
        
        try:
            # Use default TTL if not specified
            if ttl is None:
                ttl = settings.CACHE_TTL_SECONDS
            
            # Check cache size and evict if necessary
            if len(self.cache) >= self.max_size:
                await self._evict_oldest()
            
            # Store value
            self.cache[key] = {
                "value": value,
                "created_at": time.time(),
                "last_accessed": time.time(),
                "ttl": ttl
            }
            
            return True
            
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete value from cache"""
        try:
            if key in self.cache:
                del self.cache[key]
                return True
            return False
            
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
            return False
    
    async def clear(self) -> bool:
        """Clear all cache"""
        try:
            self.cache.clear()
            return True
            
        except Exception as e:
            logger.error(f"Cache clear error: {e}")
            return False
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        try:
            current_time = time.time()
            total_entries = len(self.cache)
            expired_entries = 0
            total_size = 0
            
            for entry in self.cache.values():
                if self._is_expired(entry):
                    expired_entries += 1
                total_size += len(str(entry["value"]))
            
            return {
                "total_entries": total_entries,
                "expired_entries": expired_entries,
                "active_entries": total_entries - expired_entries,
                "max_size": self.max_size,
                "cache_size_bytes": total_size,
                "enabled": self.enabled
            }
            
        except Exception as e:
            logger.error(f"Cache stats error: {e}")
            return {"error": str(e)}
    
    def _is_expired(self, cache_entry: Dict[str, Any]) -> bool:
        """Check if cache entry is expired"""
        current_time = time.time()
        created_at = cache_entry["created_at"]
        ttl = cache_entry["ttl"]
        
        return (current_time - created_at) > ttl
    
    async def _evict_oldest(self):
        """Evict oldest cache entries"""
        try:
            # Sort by last accessed time
            sorted_entries = sorted(
                self.cache.items(),
                key=lambda x: x[1]["last_accessed"]
            )
            
            # Remove 10% of oldest entries
            evict_count = max(1, len(sorted_entries) // 10)
            
            for i in range(evict_count):
                if i < len(sorted_entries):
                    key = sorted_entries[i][0]
                    del self.cache[key]
            
            logger.info(f"Evicted {evict_count} cache entries")
            
        except Exception as e:
            logger.error(f"Cache eviction error: {e}")
    
    async def cleanup_expired(self):
        """Remove expired entries from cache"""
        try:
            expired_keys = []
            
            for key, entry in self.cache.items():
                if self._is_expired(entry):
                    expired_keys.append(key)
            
            for key in expired_keys:
                del self.cache[key]
            
            if expired_keys:
                logger.info(f"Cleaned up {len(expired_keys)} expired cache entries")
                
        except Exception as e:
            logger.error(f"Cache cleanup error: {e}")


# Create global instance
cache_service = CacheService()
