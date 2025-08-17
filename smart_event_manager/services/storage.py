from __future__ import annotations
import json, os
from typing import List, Optional
from models.event import Event

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "events.json")

class Storage:
    @staticmethod
    def _ensure_file():
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "w") as f:
                json.dump([], f)

    @staticmethod
    def load() -> List[Event]:
        Storage._ensure_file()
        with open(DATA_FILE, "r") as f:
            items = json.load(f)
            return [Event.from_dict(i) for i in items]

    @staticmethod
    def save(events: List[Event]) -> None:
        Storage._ensure_file()
        with open(DATA_FILE, "w") as f:
            json.dump([e.to_dict() for e in events], f, indent=2)

    @staticmethod
    def find_by_id(events: List[Event], event_id: str) -> Optional[Event]:
        for e in events:
            if e.id == event_id:
                return e
        return None

    @staticmethod
    def find_by_name(events: List[Event], name: str) -> Optional[Event]:
        name_low = name.lower().strip()
        for e in events:
            if e.name.lower().strip() == name_low:
                return e
        return None
