from typing import List, Dict, Any
from collections import defaultdict, Counter
from .models import Launch, Rocket, Launchpad
from .util import parse_date

def calculate_success_rate_by_rocket(launches: List[Launch], rockets: List[Rocket]) -> Dict[str, Dict[str, Any]]:
    rocket_launches = defaultdict(lambda: {'total': 0, 'successful': 0})
    
    for launch in launches:
        if not launch.upcoming and launch.success is not None:
            rocket_launches[launch.rocket]['total'] += 1
            if launch.success:
                rocket_launches[launch.rocket]['successful'] += 1
    
    rocket_id_to_name = {rocket.id: rocket.name for rocket in rockets}
    result = {}
    
    for rocket_id, stats in rocket_launches.items():
        if stats['total'] > 0:
            success_rate = (stats['successful'] / stats['total']) * 100
        else:
            success_rate = 0
        
        result[rocket_id_to_name.get(rocket_id, rocket_id)] = {
            'success_rate': success_rate,
            'total_launches': stats['total'],
            'successful_launches': stats['successful']
        }
    
    return result

def count_launches_by_site(launches: List[Launch], launchpads: List[Launchpad]) -> Dict[str, int]:
    launchpad_launches = Counter()
    
    for launch in launches:
        if not launch.upcoming:
            launchpad_launches[launch.launchpad] += 1
    
    launchpad_id_to_name = {launchpad.id: launchpad.name for launchpad in launchpads}
    return {launchpad_id_to_name.get(id, id): count for id, count in launchpad_launches.items()}

def calculate_launch_frequency(launches: List[Launch]) -> Dict[str, Dict[str, int]]:
    monthly_launches = defaultdict(int)
    yearly_launches = defaultdict(int)
    
    for launch in launches:
        if not launch.upcoming:
            try:
                launch_date = parse_date(launch.date_utc)
                year = launch_date.year
                month_year = f"{launch_date.year}-{launch_date.month:02d}"
                
                yearly_launches[year] += 1
                monthly_launches[month_year] += 1
            except (ValueError, TypeError):
                continue
    
    return {
        'monthly': dict(monthly_launches),
        'yearly': dict(yearly_launches)
    }

def get_launch_statistics(launches: List[Launch]) -> Dict[str, Any]:
    total_launches = len([l for l in launches if not l.upcoming])
    successful_launches = len([l for l in launches if not l.upcoming and l.success])
    failed_launches = len([l for l in launches if not l.upcoming and l.success is False])
    upcoming_launches = len([l for l in launches if l.upcoming])
    
    success_rate = (successful_launches / total_launches * 100) if total_launches > 0 else 0
    
    return {
        'total_launches': total_launches,
        'successful_launches': successful_launches,
        'failed_launches': failed_launches,
        'upcoming_launches': upcoming_launches,
        'success_rate': success_rate
    }