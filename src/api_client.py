import requests
from typing import List, Dict, Any, Optional

from .models import Launch, Rocket, Launchpad


class SpaceXAPIClient:
    BASE_URL = "https://api.spacexdata.com/v4"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'SpaceXLaunchTracker/1.0'
        })
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Any:
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            pass
    
    def get_all_launches(self) -> List[Launch]:
        data = self._make_request("launches")
        launches = []
        for launch_data in data:
            fields = {k: v for k, v in launch_data.items() 
                          if k in Launch.__annotations__}
            
            launches.append(Launch(**fields))
        return launches
    
    def get_launch_by_id(self, launch_id: str) -> Launch:
        data = self._make_request(f"launches/{launch_id}")
         
        fields = {k: v for k, v in data.items() 
                      if k in Launch.__annotations__}
        return Launch(**fields)
    
    def get_all_rockets(self) -> List[Rocket]:
        data = self._make_request("rockets")
        rockets = []
        for rocket_data in data:
            fields = {k: v for k, v in rocket_data.items() 
                          if k in Rocket.__annotations__}
            rockets.append(Rocket(**fields))
        return rockets
    
    def get_rocket_by_id(self, rocket_id: str) -> Rocket:
        data = self._make_request(f"rockets/{rocket_id}")
        fields = {k: v for k, v in data.items() 
                      if k in Rocket.__annotations__}
        
        return Rocket(**fields)
    
    def get_all_launchpads(self) -> List[Launchpad]:
        data = self._make_request("launchpads")
        launchpads = []
        for launchpad_data in data:
            fields = {k: v for k, v in launchpad_data.items() 
                          if k in Launchpad.__annotations__}
            launchpads.append(Launchpad(**fields))
        return launchpads
    
    def get_launchpad_by_id(self, launchpad_id: str) -> Launchpad:
        data = self._make_request(f"launchpads/{launchpad_id}")
        
        fields = {k: v for k, v in data.items() 
                      if k in Launchpad.__annotations__}
        
        return Launchpad(**fields)