from app.schemas import BriefingContext


def build_morning_brief(context: BriefingContext) -> str:
    parts = []

    parts.append("Good morning.")

    if context.calendar.total_events == 0:
        parts.append("You have no calendar events today.")
    else:
        parts.append(f"You have {context.calendar.total_events} event{'s' if context.calendar.total_events != 1 else ''} today.")
        if context.calendar.first_event_time:
            first_title = context.calendar.events[0].title if context.calendar.events else "your first meeting"
            parts.append(f"Your first event is at {context.calendar.first_event_time}: {first_title}.")

    if context.email.unread_count == 0:
        parts.append("You have no unread emails.")
    else:
        parts.append(f"You have {context.email.unread_count} unread emails.")
        if context.email.top_items:
            top = context.email.top_items[0]
            parts.append(f"Top email: {top.subject} from {top.from_name}.")

    if context.weather.current_temp_f is not None and context.weather.condition:
        parts.append(
            f"It is {context.weather.current_temp_f} degrees Fahrenheit and {context.weather.condition.lower()} right now."
        )
    if context.weather.precipitation_probability_max is not None:
        parts.append(f"Rain chance today is {context.weather.precipitation_probability_max} percent.")

    parts.append("That is your morning briefing.")

    return " ".join(parts)