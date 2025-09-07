from typing import List

from .api_client import SpaceXAPIClient
from .models import Launch, Rocket, Launchpad

api_client = SpaceXAPIClient()

def get_launches() -> List[Launch]:
    launches = api_client.get_all_launches()
    return launches

def get_rockets() -> List[Rocket]:
    rockets = api_client.get_all_rockets()
    return rockets

def get_launchpads() -> List[Launchpad]:
    launchpads = api_client.get_all_launchpads()
    return launchpads

if __name__ == "__main__":
    print(get_launches())
    print(get_rockets())
    print(get_launchpads())