"""Cache manager for storing and retrieving arXiv query results."""

import json
import time
import os
from typing import Dict, Any, Optional

class CacheManager:
    def __init__(self, cache_file: str, cache_duration: int):
        self.cache_file = cache_file
        self.cache_duration = cache_duration

    def _load_cache(self) -> Dict[str, Any]:
        """Load the cache from file."""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            return {}
        except json.JSONDecodeError:
            return {}

    def _save_cache(self, cache_data: Dict[str, Any]) -> None:
        """Save the cache to file."""
        with open(self.cache_file, 'w') as f:
            json.dump(cache_data, f)

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Retrieve data from cache if it exists and is not expired."""
        cache = self._load_cache()
        if key in cache:
            entry = cache[key]
            if time.time() - entry['timestamp'] < self.cache_duration:
                return entry['data']
        return None

    def set(self, key: str, data: Dict[str, Any]) -> None:
        """Store data in cache with timestamp."""
        cache = self._load_cache()
        cache[key] = {
            'timestamp': time.time(),
            'data': data
        }
        self._save_cache(cache)
