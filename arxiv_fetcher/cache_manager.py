"""Cache manager for storing API responses."""

import json
import time
from typing import Optional, Dict, Any
import os

class CacheManager:
    def __init__(self, cache_file: str, cache_duration: int):
        self.cache_file = cache_file
        self.cache_duration = cache_duration

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if it exists and is not expired."""
        if not os.path.exists(self.cache_file):
            return None

        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                cache = json.load(f)
                if key in cache:
                    entry = cache[key]
                    if time.time() - entry['timestamp'] < self.cache_duration:
                        return entry['data']
        except (json.JSONDecodeError, KeyError, TypeError):
            return None
        return None

    def set(self, key: str, value: Any) -> None:
        """Set value in cache with current timestamp."""
        cache: Dict[str, Any] = {}
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    cache = json.load(f)
            except json.JSONDecodeError:
                pass

        cache[key] = {
            'timestamp': time.time(),
            'data': value
        }

        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache, f)
