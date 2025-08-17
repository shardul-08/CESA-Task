#!/usr/bin/env python3
import argparse
from datetime import datetime, timedelta
from getpass import getpass
from typing import List
from models.event import Event
from services.storage import Storage
from services.conflict_checker import detect_conflicts, suggest_next_slot
from services.excel_reader import load_emails_from_excel
from services.mailer import send_reminders
from utils.validators import validate_date, validate_time
from utils.cli_helpers import print_events, print_info, print_warn, print_error

ADMIN_USER = "admin"  # override via .env
import os
from dotenv import load_dotenv
load_dotenv()
ADMIN_USER = os.getenv("ADMIN_USER", ADMIN_USER)
ADMIN_PASS = os.getenv("ADMIN_PASS", None)

def require_admin():
    user = input("Admin username: ").strip()
    pwd = getpass("Admin password: ").strip()
    exp_user = ADMIN_USER
    exp_pass = ADMIN_PASS
    if exp_pass is None:
        print_warn("ADMIN_PASS not set in .env; using default 'admin' for demo purposes.")
        exp_pass = "admin"
    if user != exp_user or pwd != exp_pass:
        print_error("Invalid admin credentials.")
        raise SystemExit(1)

def parse_args():
    p = argparse.ArgumentParser(prog="SmartEventManager", description="CLI-based Smart Event Manager")
    sub = p.add_subparsers(dest="cmd", required=True)

    add = sub.add_parser("add", help="Add a new event (admin only)")
    add.add_argument("--name", required=True)
    add.add_argument("--date", required=True, help="DD-MM-YYYY")
    add.add_argument("--time", required=True, help="HH:MM 24h")
    add.add_argument("--type", required=True, dest="event_type")
    add.add_argument("--location", default="")
    add.add_argument("--duration", type=int, default=60, help="Duration in minutes")

    edit = sub.add_parser("edit", help="Edit an existing event (admin only)")
    edit.add_argument("--id", help="Event ID")
    edit.add_argument("--name", help="Event name (alternative to --id)")
    edit.add_argument("--new-name")
    edit.add_argument("--date", help="DD-MM-YYYY")
    edit.add_argument("--time", help="HH:MM")
    edit.add_argument("--type", dest="event_type")
    edit.add_argument("--location")
    edit.add_argument("--duration", type=int)

    delete = sub.add_parser("delete", help="Delete an event (admin only)")
    delete.add_argument("--id")
    delete.add_argument("--name")

    day = sub.add_parser("day", help="View events for a given date")
    day.add_argument("--date", required=True, help="DD-MM-YYYY")

    sub.add_parser("today", help="View today's events")

    search = sub.add_parser("search", help="Search events by keyword in name or type")
    search.add_argument("--q", required=True)

    remind = sub.add_parser("remind", help="Send reminder emails for upcoming events (admin only)")
    remind.add_argument("--in-days", type=int, default=1, help="Upcoming within N days (default 1)")
    remind.add_argument("--excel", default=os.path.join(os.path.dirname(__file__), "data", "attendees.xlsx"),
                        help="Path to attendees .xlsx (emails in first column)")

    sub.add_parser("stats", help="View statistics")

    return p.parse_args()

def load_events() -> List[Event]:
    return Storage.load()

def save_events(events: List[Event]) -> None:
    Storage.save(events)

def find_event(events: List[Event], id_: str = None, name: str = None) -> Event:
    if id_:
        e = Storage.find_by_id(events, id_)
        if e: return e
    if name:
        e = Storage.find_by_name(events, name)
        if e: return e
    print_error("Event not found.")
    raise SystemExit(1)

def main():
    args = parse_args()
    events = load_events()

    if args.cmd == "add":
        require_admin()
        try:
            d = validate_date(args.date)
            t = validate_time(args.time)
        except Exception as e:
            print_error(f"Invalid date/time: {e}")
            raise SystemExit(1)

        new_event = Event(name=args.name, date=d, time=t, event_type=args.event_type,
                          location=args.location, duration_min=args.duration)
        dup = [e for e in events if e.name.strip().lower() == new_event.name.strip().lower() and e.start_dt()==new_event.start_dt()]
        if dup:
            print_error("Duplicate event exists with the same name and start time.")
            raise SystemExit(1)

        conflicts = detect_conflicts(events, new_event)
        if conflicts:
            print_warn("Scheduling conflict detected with:")
            print_events(conflicts, title="Conflicting Events")
            suggestion = suggest_next_slot(events, new_event.date, new_event.duration_min)
            if suggestion:
                print_warn(f"Suggested available start time on {new_event.date}: {suggestion}")
            raise SystemExit(1)

        events.append(new_event)
        save_events(events)
        print_info("Event added successfully.")
        print_events([new_event], title="Added Event")

    elif args.cmd == "edit":
        require_admin()
        target = find_event(events, args.id, args.name)
        if args.new_name: target.name = args.new_name
        if args.date:     target.date = validate_date(args.date)
        if args.time:     target.time = validate_time(args.time)
        if args.event_type: target.event_type = args.event_type
        if args.location is not None: target.location = args.location
        if args.duration is not None: target.duration_min = int(args.duration)

        conflicts = detect_conflicts(events, target)
        if conflicts:
            print_warn("Edit introduces a conflict with:")
            print_events(conflicts, title="Conflicting Events")
            suggestion = suggest_next_slot(events, target.date, target.duration_min)
            if suggestion:
                print_warn(f"Suggested available start time on {target.date}: {suggestion}")
            raise SystemExit(1)

        save_events(events)
        print_info("Event updated successfully.")
        print_events([target], title="Updated Event")

    elif args.cmd == "delete":
        require_admin()
        target = find_event(events, args.id, args.name)
        events = [e for e in events if e.id != target.id]
        save_events(events)
        print_info("Event deleted.")
        print_events([target], title="Deleted Event")

    elif args.cmd == "day":
        try:
            d = validate_date(args.date)
        except Exception as e:
            print_error(f"Invalid date: {e}")
            raise SystemExit(1)
        day_events = [e for e in events if e.date == d]
        print_events(sorted(day_events, key=lambda e: e.start_dt()), title=f"Events on {d}")

    elif args.cmd == "today":
        today = datetime.now().strftime("%d-%m-%Y")
        today_events = [e for e in events if e.date == today]
        print_events(sorted(today_events, key=lambda e: e.start_dt()), title=f"Today's Events ({today})")

    elif args.cmd == "search":
        q = args.q.lower().strip()
        result = [e for e in events if q in e.name.lower() or q in e.event_type.lower()]
        print_events(result, title=f"Search Results for '{args.q}'")

    elif args.cmd == "remind":
        require_admin()
        now = datetime.now()
        edge = now + timedelta(days=int(args.in_days))
        upcoming = [e for e in events if now <= e.start_dt() <= edge]
        if not upcoming:
            print_warn("No upcoming events in the given window.")
            return
        try:
            recipients = load_emails_from_excel(args.excel)
        except Exception as e:
            print_error(f"Failed to load emails from Excel: {e}")
            raise SystemExit(1)

        for ev in upcoming:
            try:
                send_reminders(ev, recipients)
                print_info(f"Reminders sent for event '{ev.name}' to {len(recipients)} recipient(s).")
            except Exception as e:
                print_error(f"Failed to send reminders: {e}")

    elif args.cmd == "stats":
        from collections import Counter
        by_type = Counter([e.event_type for e in events])
        by_date = Counter([e.date for e in events])
        print_info("Events by type:")
        for t, c in by_type.items():
            print(f"  - {t}: {c}")
        print_info("Events by date:")
        for d, c in sorted(by_date.items()):
            print(f"  - {d}: {c}")

if __name__ == "__main__":
    main()
