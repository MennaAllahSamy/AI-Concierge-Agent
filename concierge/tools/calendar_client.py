"""Read-only Google Calendar client. Exposes only list/read operations."""

import datetime
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Read-only scope — the token itself cannot modify the calendar.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.json"


def _get_service():
    """Authenticate (once) and return a Calendar API service object."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
    return build("calendar", "v3", credentials=creds)


def list_events(max_results: int = 10):
    """Return upcoming events from the user's primary calendar."""
    service = _get_service()
    now = datetime.datetime.utcnow().isoformat() + "Z"
    result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = result.get("items", [])
    return [
        {
            "start": e["start"].get("dateTime", e["start"].get("date")),
            "summary": e.get("summary", "(no title)"),
        }
        for e in events
    ]
def find_free_slots(date: str, day_start_hour: int = 9, day_end_hour: int = 18):
    """Find free time gaps on a given date (YYYY-MM-DD) between working hours.

    Returns a list of {"start": ..., "end": ...} slots where nothing is scheduled.
    Read-only: it inspects events but never modifies the calendar.
    """
    service = _get_service()

    day_start = datetime.datetime.fromisoformat(f"{date}T{day_start_hour:02d}:00:00")
    day_end = datetime.datetime.fromisoformat(f"{date}T{day_end_hour:02d}:00:00")

    result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=day_start.isoformat() + "Z",
            timeMax=day_end.isoformat() + "Z",
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = result.get("items", [])

    busy = []
    for e in events:
        start = e["start"].get("dateTime")
        end = e["end"].get("dateTime")
        if start and end:
            busy.append(
                (
                    datetime.datetime.fromisoformat(start).replace(tzinfo=None),
                    datetime.datetime.fromisoformat(end).replace(tzinfo=None),
                )
            )

    free = []
    cursor = day_start
    for start, end in busy:
        if start > cursor:
            free.append({"start": cursor.isoformat(), "end": start.isoformat()})
        cursor = max(cursor, end)
    if cursor < day_end:
        free.append({"start": cursor.isoformat(), "end": day_end.isoformat()})

    return free
def create_calendar_event(summary: str, start: str, end: str):
    """Create a calendar event. (Demo stub — does not really write.)

    A WRITE action. This must pass through the confirmation gate before it runs.
    """
    return {
        "status": "created",
        "summary": summary,
        "start": start,
        "end": end,
    }