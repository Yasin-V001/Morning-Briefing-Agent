from email.utils import parseaddr

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from app.config import settings
from app.schemas import EmailSummary, EmailItem
from app.services.google_auth import load_credentials


SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def _get_gmail_service():
    creds = load_credentials(SCOPES)
    return build("gmail", "v1", credentials=creds)


def _header_value(headers, name):
    for h in headers:
        if h.get("name", "").lower() == name.lower():
            return h.get("value", "")
    return ""


async def fetch_email_summary() -> EmailSummary:
    service = _get_gmail_service()

    query = "is:unread in:inbox -category:promotions -category:social -label:spam"
    result = service.users().messages().list(userId="me", q=query, maxResults=5).execute()
    messages = result.get("messages", [])

    unread_count_result = service.users().messages().list(userId="me", q=query, maxResults=100).execute()
    unread_count = len(unread_count_result.get("messages", []))

    top_items = []

    for msg in messages[:3]:
        full = service.users().messages().get(userId="me", id=msg["id"], format="metadata").execute()
        payload = full.get("payload", {})
        headers = payload.get("headers", [])

        subject = _header_value(headers, "Subject") or "(No subject)"
        from_header = _header_value(headers, "From") or "Unknown sender"
        from_name, from_email = parseaddr(from_header)
        snippet = full.get("snippet", "")

        top_items.append(
            EmailItem(
                from_name=from_name or from_email or "Unknown sender",
                subject=subject,
                snippet=snippet,
            )
        )

    return EmailSummary(
        unread_count=unread_count,
        top_items=top_items,
    )