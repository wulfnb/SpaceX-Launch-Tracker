from datetime import date, datetime

def parse_date(launch_date):
    try:
        if '.' in launch_date and 'Z' in launch_date:
            return datetime.strptime(launch_date, "%Y-%m-%dT%H:%M:%S.%fZ").date()
        else:
            return  datetime.strptime(launch_date, "%Y-%m-%dT%H:%M:%SZ").date()
    except (ValueError, TypeError):
        return date(1900, 1, 1)