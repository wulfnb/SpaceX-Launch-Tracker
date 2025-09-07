from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

@dataclass
class Rocket:
    id: str
    name: str
    type: str
    active: bool
    stages: int
    boosters: int
    cost_per_launch: int
    success_rate_pct: int
    first_flight: str
    country: str
    company: str
    height: Dict[str, float]
    diameter: Dict[str, float]
    mass: Dict[str, int]
    payload_weights: List[Dict[str, Any]] = field(default_factory=list)
    first_stage: Dict[str, Any] = field(default_factory=dict)
    second_stage: Dict[str, Any] = field(default_factory=dict)
    engines: Dict[str, Any] = field(default_factory=dict)
    landing_legs: Dict[str, Any] = field(default_factory=dict)
    flickr_images: List[str] = field(default_factory=list)
    wikipedia: str = ""
    description: str = ""

@dataclass
class Launchpad:
    id: str
    name: str
    full_name: str
    status: str
    locality: str
    region: str
    timezone: str
    latitude: float
    longitude: float
    launch_attempts: int
    launch_successes: int
    rockets: List[str] = field(default_factory=list)
    launches: List[str] = field(default_factory=list)
    details: str = ""
    
@dataclass
class Launch:
    id: str
    flight_number: int
    name: str
    date_utc: str
    date_unix: int
    date_local: str
    date_precision: str
    static_fire_date_utc: Optional[str] = None
    static_fire_date_unix: Optional[int] = None
    tbd: bool = False
    net: bool = False
    window: Optional[int] = None
    rocket: str = ""
    success: Optional[bool] = None
    failures: List[Dict[str, Any]] = field(default_factory=list)
    upcoming: bool = False
    details: Optional[str] = None
    fairings: Optional[Dict[str, Any]] = None
    crew: List[str] = field(default_factory=list)
    ships: List[str] = field(default_factory=list)
    capsules: List[str] = field(default_factory=list)
    payloads: List[str] = field(default_factory=list)
    launchpad: str = ""
    cores: List[Dict[str, Any]] = field(default_factory=list)
    links: Dict[str, Any] = field(default_factory=dict)
    auto_update: bool = False