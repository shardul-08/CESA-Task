from datetime import datetime

DATE_FMT = "%d-%m-%Y"
TIME_FMT = "%H:%M"

def validate_date(date_str: str) -> str:
    dt = datetime.strptime(date_str, DATE_FMT)  # raises if invalid
    return dt.strftime(DATE_FMT)

def validate_time(time_str: str) -> str:
    tm = datetime.strptime(time_str, TIME_FMT)
    return tm.strftime(TIME_FMT)
