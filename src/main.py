from typing import List

from .cache_manager import CacheManager
from .models import Launch, Rocket, Launchpad

cache_manager = CacheManager()

def get_launches() -> List[Launch]:
    launches = cache_manager.get_launches()
    return launches

def get_rockets() -> List[Rocket]:
    rockets = cache_manager.get_rockets()
    return rockets

def get_launchpads() -> List[Launchpad]:
    launchpads = cache_manager.get_launchpads()
    return launchpads

if __name__ == "__main__":
    print(get_launches())
    print(get_rockets())
    print(get_launchpads())