from app.schemas import CalendarSummary, CalendarEvent
from app.config import settings
from app.utils.datetime_utils import today_local_date_str


async def fetch_calendar_summary() -> CalendarSummary:
    return CalendarSummary(
        date=today_local_date_str(settings.timezone),
        timezone=settings.timezone,
        total_events=2,
        first_event_time="09:00 AM",
        events=[
            CalendarEvent(
                title="Standup",
                start="2026-04-21T09:00:00",
                end="2026-04-21T09:30:00",
                location="Google Meet",
            ),
            CalendarEvent(
                title="Design Review",
                start="2026-04-21T14:00:00",
                end="2026-04-21T15:00:00",
                location="Zoom",
            ),
        ],
    )