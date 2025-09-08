import argparse
from datetime import datetime, date
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

def filter_by_date_range(launches: List[Launch], start_date: date, end_date: date) -> List[Launch]:
    def in_date_range(launch: Launch) -> bool:
        try:
            if '.' in launch.date_utc and 'Z' in launch.date_utc:
                launch_date = datetime.strptime(launch.date_utc, "%Y-%m-%dT%H:%M:%S.%fZ").date()
            else:
                launch_date =  datetime.strptime(launch.date_utc, "%Y-%m-%dT%H:%M:%SZ").date()
        except (ValueError, TypeError):
            launch_date = date(1900, 1, 1)
        return start_date <= launch_date <= end_date
    
    return list(filter(in_date_range, launches))


def filter_by_rocket(launches: List[Launch], rocket_id: str) -> List[Launch]:
    return [launch for launch in launches if launch.rocket == rocket_id]


def filter_by_success(launches: List[Launch], success: bool) -> List[Launch]:
    return [launch for launch in launches if launch.success == success and not launch.upcoming]


def filter_by_launchpad(launches: List[Launch], launchpad_id: str) -> List[Launch]:
    return [launch for launch in launches if launch.launchpad == launchpad_id]


def filter_upcoming(launches: List[Launch]) -> List[Launch]:
    return [launch for launch in launches if launch.upcoming]


def filter_completed(launches: List[Launch]) -> List[Launch]:
    return [launch for launch in launches if not launch.upcoming]

def apply_filters(launches: List[Launch], **filters) -> List[Launch]:
    filtered_launches = launches
    if 'start_date' in filters and 'end_date' in filters:
        filtered_launches = filter_by_date_range(
            filtered_launches, filters['start_date'], filters['end_date']
        )
    if 'rocket_id' in filters:
        filtered_launches = filter_by_rocket(
            filtered_launches, filters['rocket_id']
        )
    if 'success' in filters:
        filtered_launches = filter_by_success(
            filtered_launches, filters['success']
        )
    if 'launchpad_id' in filters:
        filtered_launches = filter_by_launchpad(
            filtered_launches, filters['launchpad_id']
        )

    if 'upcoming' in filters and filters['upcoming']:
        filtered_launches = filter_upcoming(filtered_launches)
    return filtered_launches

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SpaceX Launch Tracker")
    parser.add_argument("--filter-rocket", help="Filter by rocket ID")
    parser.add_argument("--filter-success", choices=["true", "false"], help="Filter by success status")
    parser.add_argument("--filter-launchpad", help="Filter by launchpad ID")
    parser.add_argument("--filter-upcoming", action="store_true", help="Show only upcoming launches")
    parser.add_argument("--start-date", help="Start date for filtering (YYYY-MM-DD)")
    parser.add_argument("--end-date", help="End date for filtering (YYYY-MM-DD)")

    
    args = parser.parse_args()
    print(args)
    launches = get_launches()
    rockets = get_rockets()
    launchpads = get_launchpads()
    
    # Apply filters
    filter_args = {}
    if args.filter_rocket:
        filter_args['rocket_id'] = args.filter_rocket
    if args.filter_success:
        filter_args['success'] = args.filter_success.lower() == "true"
    if args.filter_launchpad:
        filter_args['launchpad_id'] = args.filter_launchpad
    if args.filter_upcoming:
        filter_args['upcoming'] = True
    if args.start_date and args.end_date:
        filter_args['start_date'] = datetime.strptime(args.start_date, "%Y-%m-%d").date()
        filter_args['end_date'] = datetime.strptime(args.end_date, "%Y-%m-%d").date()
    
    filtered_launches = apply_filters(launches, **filter_args)

    print(filtered_launches)
    # print(rockets)
    # print(launchpads)