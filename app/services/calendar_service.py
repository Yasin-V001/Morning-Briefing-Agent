from datetime import datetime
from zoneinfo import ZoneInfo

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from app.config import settings
from app.schemas import CalendarSummary, CalendarEvent
from app.utils.datetime_utils import today_bounds_iso, today_local_date_str
from app.services.google_auth import load_credentials

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def _get_calendar_service():
    creds = load_credentials(SCOPES)
    return build("calendar", "v3", credentials=creds)


async def fetch_calendar_summary() -> CalendarSummary:
    service = _get_calendar_service()
    time_min, time_max = today_bounds_iso(settings.timezone)

    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    items = events_result.get("items", [])
    events = []

    for item in items:
        start_raw = item["start"].get("dateTime", item["start"].get("date"))
        end_raw = item["end"].get("dateTime", item["end"].get("date"))
        title = item.get("summary", "Untitled event")
        location = item.get("location")

        events.append(
            CalendarEvent(
                title=title,
                start=start_raw,
                end=end_raw,
                location=location,
            )
        )

    first_event_time = None
    if items:
        start_dt_raw = items[0]["start"].get("dateTime")
        if start_dt_raw:
            dt = datetime.fromisoformat(start_dt_raw.replace("Z", "+00:00"))
            dt_local = dt.astimezone(ZoneInfo(settings.timezone))
            first_event_time = dt_local.strftime("%I:%M %p")

    return CalendarSummary(
        date=today_local_date_str(settings.timezone),
        timezone=settings.timezone,
        total_events=len(events),
        first_event_time=first_event_time,
        events=events,
    )