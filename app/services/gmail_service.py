from app.schemas import EmailSummary, EmailItem


async def fetch_email_summary() -> EmailSummary:
    return EmailSummary(
        unread_count=3,
        top_items=[
            EmailItem(
                from_name="Alex",
                subject="Need approval before noon",
                snippet="Can you review the final version this morning?",
            ),
            EmailItem(
                from_name="Sarah",
                subject="Launch checklist",
                snippet="Please confirm owners for the remaining tasks.",
            ),
        ],
    )