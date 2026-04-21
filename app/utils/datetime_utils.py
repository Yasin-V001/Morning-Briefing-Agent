from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def now_local(timezone_name: str) -> datetime:
    return datetime.now(ZoneInfo(timezone_name))


def today_local_date_str(timezone_name: str) -> str:
    return now_local(timezone_name).date().isoformat()


def today_bounds_iso(timezone_name: str) -> tuple[str, str]:
    now = now_local(timezone_name)
    start = datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=ZoneInfo(timezone_name))
    end = start + timedelta(days=1)
    return start.isoformat(), end.isoformat()