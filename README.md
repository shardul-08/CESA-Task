What is inside the file ?
main.py — CLI entry point (argparse)

models/ — Event, User classes

services/ — JSON storage, conflict detection, Excel reader, email sender

utils/ — validators and pretty CLI helpers (uses rich)

data/ — events.json (storage) + sample attendees.xlsx

requirements.txt, .env.example, README.md



HOW TO RUN IT ??
Running it Locally

unzip smart_event_manager.zip
cd smart_event_manager
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt



Sample Commands

# (Admin-only; default demo creds admin/admin if not set)
python main.py add --name "Team Sync" --date 18-08-2025 --time 14:00 --type Work --location Zoom --duration 45
python main.py day --date 18-08-2025
python main.py today
python main.py search --q team
python main.py stats

# Send reminders to emails in data/attendees.xlsx for events in the next 1 day
python main.py remind --in-days 1 --excel data/attendees.xlsx

cp .env.example .env         # edit ADMIN_* and SMTP_* if needed





