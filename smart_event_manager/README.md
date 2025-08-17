# Smart Event Manager (CLI-Based)

A command-line Smart Event Manager showcasing OOP, file handling, conflict detection, reminders (Excel + email), and admin controls.

## ✨ Features
- Add / Edit / Delete events (**admin-only**)
- View by day and **Today**
- **Conflict detection** with **suggested next available slot**
- **Search** by keyword (name or type, case-insensitive)
- **Event reminders**: reads attendee emails from `.xlsx` and sends via SMTP
- **Persistent storage** using `data/events.json`
- **Admin Control** via credentials in `.env`
- **Statistics** by type and date
- Polished output via `rich`

## 📦 Project Structure
```
smart_event_manager/
├── main.py
├── models/
│   ├── event.py
│   └── user.py
├── services/
│   ├── storage.py
│   ├── conflict_checker.py
│   ├── mailer.py
│   └── excel_reader.py
├── utils/
│   ├── validators.py
│   └── cli_helpers.py
├── data/
│   ├── events.json
│   └── attendees.xlsx
├── requirements.txt
├── .env.example
└── README.md
```

## 🚀 Quick Start

```bash
# 1) Create and activate a virtualenv (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Configure admin and email (copy and edit .env.example)
cp .env.example .env
# set ADMIN_USER, ADMIN_PASS, SMTP_* if you want to send emails

# 4) Run a few sample commands
python main.py add --name "Team Sync" --date 18-08-2025 --time 14:00 --type Work --location Zoom --duration 45
python main.py day --date 18-08-2025
python main.py search --q team
python main.py today
python main.py stats

# 5) Send reminders for events happening in the next 1 day
python main.py remind --in-days 1 --excel data/attendees.xlsx
```

> **Note:** Commands that modify data or send emails are **admin-only**. You'll be prompted for credentials based on values in `.env` (defaults to `admin/admin` if not set, for demo).

## 🛠️ Inputs & Validation
- Date format: `DD-MM-YYYY`
- Time format: `HH:MM` (24h)
- Duplicate prevention: same `name` + same start datetime
- Conflict detection: events are considered overlapping if their time ranges overlap. Default duration is 60 min (configurable with `--duration`).

## 🔐 Admin-Only Commands
- `add`, `edit`, `delete`, `remind`
- Admin is prompted for username & password (from `.env`).

## 📧 Reminders & Excel
- Put attendee emails in the **first column** of `data/attendees.xlsx` (one per row).
- Configure SMTP in `.env`. Example for Gmail:
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=youraddress@gmail.com
SMTP_PASS=xxxx app password xxxx
MAIL_FROM=Smart Event Manager <youraddress@gmail.com>
```
> For Gmail, create an **App Password** with 2FA enabled.

## 📊 Sample CLI Commands
```bash
# Add
python main.py add --name "Client Demo" --date 20-08-2025 --time 11:00 --type "Business" --location "Office" --duration 90

# Edit (by id or name)
python main.py edit --name "Client Demo" --time 12:00
python main.py edit --id 1a2b3c4d --date 21-08-2025 --duration 60

# Delete
python main.py delete --name "Client Demo"

# View
python main.py day --date 21-08-2025
python main.py today

# Search
python main.py search --q demo

# Reminders (next 2 days)
python main.py remind --in-days 2 --excel data/attendees.xlsx

# Stats
python main.py stats
```

## 🧪 Screenshots
Run the above commands and capture terminal output screenshots for your submission.

## ✅ Evaluation Notes
- Modular OOP design and JSON-based persistence
- Accurate conflict detection & suggested time slots (30-min increments within 08:00–18:00)
- Robust validation and admin gating
- Mail integration with Excel attendees

## 👣 Roadmap / Bonus Ideas
- Recurring events (RRULE)
- iCal export
- SQLite backend option
- Unit tests with `pytest`
- Better interactive TUI with `textual`
