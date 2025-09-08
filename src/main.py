import argparse
from datetime import datetime, date
from typing import List, Dict, Any
from tabulate import tabulate
import json

from .cache_manager import CacheManager
from .models import Launch, Rocket, Launchpad
from .util import parse_date
from .statistics import calculate_launch_frequency, calculate_success_rate_by_rocket, get_launch_statistics

cache_manager = CacheManager()

def display_launches(launches: List[Launch], rockets: List[Rocket], launchpads: List[Launchpad]) -> None:
    """Display launches in a formatted table"""
    if not launches:
        print("No launches found matching the criteria.")
        return
    
    # Create mappings for IDs to names
    rocket_id_to_name = {rocket.id: rocket.name for rocket in rockets}
    launchpad_id_to_name = {launchpad.id: launchpad.name for launchpad in launchpads}
    
    table_data = []
    for launch in launches:
        status = "Upcoming" if launch.upcoming else "Success" if launch.success else "Failure"
        
        table_data.append([
            launch.flight_number,
            launch.name,
            launch.date_utc[:10],  # Just the date part
            rocket_id_to_name.get(launch.rocket, launch.rocket),
            launchpad_id_to_name.get(launch.launchpad, launch.launchpad),
            status
        ])
    
    headers = ["Flight #", "Name", "Date", "Rocket", "Launch Site", "Status"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

def display_statistics(statistics: Dict[str, Any]) -> None:
    """Display statistics in a formatted way"""
    print("\n=== LAUNCH STATISTICS ===")
    print(f"Total launches: {statistics['total_launches']}")
    print(f"Successful launches: {statistics['successful_launches']}")
    print(f"Failed launches: {statistics['failed_launches']}")
    print(f"Upcoming launches: {statistics['upcoming_launches']}")
    print(f"Success rate: {statistics['success_rate']:.2f}%")

def display_success_rates(success_rates: Dict[str, Dict[str, Any]]) -> None:
    """Display success rates by rocket"""
    if not success_rates:
        print("No success rate data available.")
        return
    
    table_data = []
    for rocket, stats in success_rates.items():
        table_data.append([
            rocket,
            stats['total_launches'],
            stats['successful_launches'],
            f"{stats['success_rate']:.2f}%"
        ])
    
    headers = ["Rocket", "Total Launches", "Successful", "Success Rate"]
    print("\n=== SUCCESS RATES BY ROCKET ===")
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

def display_launch_frequency(frequency_data: Dict[str, Dict[str, int]]) -> None:
    """Display launch frequency data"""
    print("\n=== LAUNCH FREQUENCY ===")
    
    # Yearly frequency
    yearly_data = frequency_data['yearly']
    if yearly_data:
        print("\nYearly Launches:")
        for year, count in sorted(yearly_data.items()):
            print(f"  {year}: {count} launches")
    
    # Monthly frequency (show only recent months)
    monthly_data = frequency_data['monthly']
    if monthly_data:
        print("\nMonthly Launches (recent):")
        recent_months = sorted(monthly_data.keys(), reverse=True)[:12]
        for month in recent_months:
            print(f"  {month}: {monthly_data[month]} launches")

def export_data(launches: List[Launch], format: str) -> None:
    if format == "json":
        data = [launch.__dict__ for launch in launches]
        filename = f"spacex_launches_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        print(f"Data exported to {filename}")
    elif format == "csv":
        import csv
        filename = f"spacex_launches_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            if launches:
                writer.writerow(launches[0].__dict__.keys())
                for launch in launches:
                    writer.writerow([str(value) for value in launch.__dict__.values()])
        print(f"Data exported to {filename}")

def get_launches(force_refresh: bool = False) -> List[Launch]:
    launches = cache_manager.get_launches(force_refresh)
    return launches

def get_rockets(force_refresh: bool = False) -> List[Rocket]:
    rockets = cache_manager.get_rockets(force_refresh)
    return rockets

def get_launchpads(force_refresh: bool = False) -> List[Launchpad]:
    launchpads = cache_manager.get_launchpads(force_refresh)
    return launchpads

def filter_by_date_range(launches: List[Launch], start_date: date, end_date: date) -> List[Launch]:
    def in_date_range(launch: Launch) -> bool:
        launch_date = parse_date(launch.date_utc)
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
    parser.add_argument("--refresh", action="store_true", help="Force refresh of cached data")
    parser.add_argument("--filter-rocket", help="Filter by rocket ID")
    parser.add_argument("--filter-success", choices=["true", "false"], help="Filter by success status")
    parser.add_argument("--filter-launchpad", help="Filter by launchpad ID")
    parser.add_argument("--filter-upcoming", action="store_true", help="Show only upcoming launches")
    parser.add_argument("--start-date", help="Start date for filtering (YYYY-MM-DD)")
    parser.add_argument("--end-date", help="End date for filtering (YYYY-MM-DD)")
    parser.add_argument("--stats", action="store_true", help="Show statistics")
    parser.add_argument("--success-rates", action="store_true", help="Show success rates by rocket")
    parser.add_argument("--frequency", action="store_true", help="Show launch frequency")
    parser.add_argument("--export", choices=["json", "csv"], help="Export data to file")
    
    args = parser.parse_args()
    print(args)
    launches = get_launches(force_refresh=args.refresh)
    rockets = get_rockets(force_refresh=args.refresh)
    launchpads = get_launchpads(force_refresh=args.refresh)
    
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
    if not any([args.stats, args.success_rates, args.frequency]):
        display_launches(filtered_launches, rockets, launchpads)
    
    if args.stats:
        stats = get_launch_statistics(filtered_launches)
        display_statistics(stats)
    
    if args.success_rates:
        success_rates = calculate_success_rate_by_rocket(
            filtered_launches, rockets
        )
        display_success_rates(success_rates)
    
    if args.frequency:
        frequency = calculate_launch_frequency(filtered_launches)
        display_launch_frequency(frequency)

    if args.export:
        export_data(filtered_launches, args.export)

