import json
import logging
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from pathlib import Path

from .api_client import SpaceXAPIClient
from .models import Launch, Rocket, Launchpad


class CacheManager:
    def __init__(self, cache_dir: str = ".cache"):
        self.api_client = SpaceXAPIClient()
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    
    def _get_cache_path(self, endpoint: str) -> Path:
        return self.cache_dir / f"{endpoint.replace('/', '_')}.json"
    
    def _is_cache_valid(self, cache_path: Path, max_age_hours: int = 24) -> bool:
        if not cache_path.exists():
            return False
        
        cache_time = datetime.fromtimestamp(cache_path.stat().st_mtime)
        return datetime.now() - cache_time < timedelta(hours=max_age_hours)
    
    def _load_from_cache(self, cache_path: Path) -> Any:
        try:
            with open(cache_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            # TODO Log
            return None
    
    def _save_to_cache(self, cache_path: Path, data: Any) -> None:
        try:
            with open(cache_path, 'w') as f:
                json.dump(data, f, default=str, indent=2)
        except IOError as e:
            # TODO Log
            pass
    
    def get_launches(self, force_refresh: bool = False) -> List[Launch]:
        cache_path = self._get_cache_path("launches")
        
        if not force_refresh and self._is_cache_valid(cache_path):
            cached_data = self._load_from_cache(cache_path)
            if cached_data:
                return [Launch(**launch) for launch in cached_data]
        
        launches = self.api_client.get_all_launches()
        
        launches_dict = [launch.__dict__ for launch in launches]
        self._save_to_cache(cache_path, launches_dict)
        
        return launches
    
    def get_rockets(self, force_refresh: bool = False) -> List[Rocket]:
        cache_path = self._get_cache_path("rockets")
        
        if not force_refresh and self._is_cache_valid(cache_path):
            cached_data = self._load_from_cache(cache_path)
            if cached_data:
                return [Rocket(**rocket) for rocket in cached_data]
        
        rockets = self.api_client.get_all_rockets()
        
        rockets_dict = [rocket.__dict__ for rocket in rockets]
        self._save_to_cache(cache_path, rockets_dict)
        
        return rockets
    
    def get_launchpads(self, force_refresh: bool = False) -> List[Launchpad]:
        cache_path = self._get_cache_path("launchpads")
        
        if not force_refresh and self._is_cache_valid(cache_path):
            cached_data = self._load_from_cache(cache_path)
            if cached_data:
                return [Launchpad(**launchpad) for launchpad in cached_data]
        
        launchpads = self.api_client.get_all_launchpads()
        
        launchpads_dict = [launchpad.__dict__ for launchpad in launchpads]
        self._save_to_cache(cache_path, launchpads_dict)
        
        return launchpads
