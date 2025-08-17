from __future__ import annotations
from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta
import uuid
from typing import Dict, Any

DATE_FMT = "%d-%m-%Y"
TIME_FMT = "%H:%M"

@dataclass
class Event:
    name: str
    date: str      # DD-MM-YYYY
    time: str      # HH:MM (24h)
    event_type: str
    location: str = ""
    duration_min: int = 60
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Event":
        return cls(**data)

    def start_dt(self) -> datetime:
        return datetime.strptime(f"{self.date} {self.time}", f"{DATE_FMT} {TIME_FMT}")

    def end_dt(self) -> datetime:
        return self.start_dt() + timedelta(minutes=self.duration_min)

    def overlaps(self, other: "Event") -> bool:
        if self.date != other.date:
            return False
        return not (self.end_dt() <= other.start_dt() or self.start_dt() >= other.end_dt())

    def __str__(self) -> str:
        end = self.end_dt().strftime(TIME_FMT)
        loc = f" @ {self.location}" if self.location else ""
        return f"[{self.id}] {self.name} | {self.date} {self.time}-{end} | {self.event_type}{loc}"
