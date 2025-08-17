from __future__ import annotations
from typing import List, Optional
from datetime import datetime, timedelta
from models.event import Event, DATE_FMT, TIME_FMT

WORK_START = "08:00"
WORK_END = "18:00"
SLOT_MINUTES = 30

def detect_conflicts(events: List[Event], target: Event) -> List[Event]:
    return [e for e in events if e.id != target.id and e.overlaps(target)]

def suggest_next_slot(events: List[Event], date: str, duration_min: int) -> Optional[str]:
    day_events = sorted([e for e in events if e.date == date], key=lambda e: e.start_dt())
    day_start = datetime.strptime(f"{date} {WORK_START}", f"{DATE_FMT} {TIME_FMT}")
    day_end   = datetime.strptime(f"{date} {WORK_END}",   f"{DATE_FMT} {TIME_FMT}")
    candidate_start = day_start

    def free_at(start) -> bool:
        dummy = Event(name="_", date=date, time=start.strftime(TIME_FMT), event_type="_", duration_min=duration_min)
        return all(not dummy.overlaps(e) for e in day_events) and start + timedelta(minutes=duration_min) <= day_end

    while candidate_start + timedelta(minutes=duration_min) <= day_end:
        if free_at(candidate_start):
            return candidate_start.strftime(TIME_FMT)
        candidate_start += timedelta(minutes=SLOT_MINUTES)
    return None
