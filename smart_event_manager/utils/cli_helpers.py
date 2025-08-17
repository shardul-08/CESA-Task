from typing import List
from models.event import Event
from rich.table import Table
from rich.console import Console

console = Console()

def print_events(events: List[Event], title: str = "Events") -> None:
    table = Table(title=title)
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name")
    table.add_column("Date")
    table.add_column("Time")
    table.add_column("End")
    table.add_column("Type")
    table.add_column("Location")
    table.add_column("Duration (min)")
    for e in sorted(events, key=lambda x: (x.date, x.time)):
        table.add_row(e.id, e.name, e.date, e.time, e.end_dt().strftime("%H:%M"),
                      e.event_type, e.location or "-", str(e.duration_min))
    console.print(table)

def print_info(msg: str):
    console.print(f"[bold green]✔ {msg}[/]")

def print_warn(msg: str):
    console.print(f"[bold yellow]⚠ {msg}[/]")

def print_error(msg: str):
    console.print(f"[bold red]✖ {msg}[/]")
