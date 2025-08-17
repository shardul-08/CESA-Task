import os, smtplib
from typing import List
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from models.event import Event
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
MAIL_FROM = os.getenv("MAIL_FROM", SMTP_USER or "no-reply@example.com")

def send_reminders(event: Event, recipients: List[str]) -> None:
    if not SMTP_USER or not SMTP_PASS:
        raise RuntimeError("SMTP_USER and SMTP_PASS must be set in .env to send emails.")
    subject = f"Reminder: {event.name} on {event.date} at {event.time}"
    body = f"""Hello,

This is a reminder for the upcoming event:

Name: {event.name}
Date: {event.date}
Time: {event.time}
Type: {event.event_type}
Location: {event.location or '-'}

See you there!
"""
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        for rcpt in recipients:
            msg = MIMEMultipart()
            msg["From"] = MAIL_FROM
            msg["To"] = rcpt
            msg["Date"] = formatdate(localtime=True)
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))
            server.sendmail(MAIL_FROM, rcpt, msg.as_string())
