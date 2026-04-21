from app.config import settings
from app.schemas import BriefingContext
from app.services.calendar_service import fetch_calendar_summary
from app.services.gmail_service import fetch_email_summary
from app.services.weather_service import fetch_weather_summary
from app.services.summarizer import build_morning_brief
from app.services.delivery_openclaw import deliver_briefing
from app.utils.datetime_utils import today_local_date_str
from app.utils.logging_utils import get_logger

logger = get_logger(__name__)


async def run_morning_briefing() -> str:
    logger.info("Starting morning briefing run.")

    calendar_summary = await fetch_calendar_summary()
    email_summary = await fetch_email_summary()
    weather_summary = await fetch_weather_summary()

    context = BriefingContext(
        date=today_local_date_str(settings.timezone),
        timezone=settings.timezone,
        calendar=calendar_summary,
        email=email_summary,
        weather=weather_summary,
    )

    briefing_text = build_morning_brief(context)
    delivered = await deliver_briefing(briefing_text)

    logger.info("Morning briefing run completed. delivered=%s", delivered)
    return briefing_text