from typing import Optional, List
from pydantic import BaseModel


class CalendarEvent(BaseModel):
    title: str
    start: str
    end: str
    location: Optional[str] = None


class CalendarSummary(BaseModel):
    date: str
    timezone: str
    total_events: int
    first_event_time: Optional[str] = None
    events: List[CalendarEvent] = []


class EmailItem(BaseModel):
    from_name: str
    subject: str
    snippet: str


class EmailSummary(BaseModel):
    unread_count: int
    top_items: List[EmailItem] = []


class WeatherSummary(BaseModel):
    current_temp_c: Optional[float] = None
    current_temp_f: Optional[float] = None
    condition: Optional[str] = None
    high_c: Optional[float] = None
    low_c: Optional[float] = None
    precipitation_probability_max: Optional[float] = None


class BriefingContext(BaseModel):
    date: str
    timezone: str
    calendar: CalendarSummary
    email: EmailSummary
    weather: WeatherSummary


class RunResult(BaseModel):
    success: bool
    message: str
    delivered: bool = False