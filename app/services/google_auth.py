from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from app.config import settings


def load_credentials(scopes: list[str]) -> Credentials:
    creds = Credentials.from_authorized_user_file(settings.google_token_file, scopes)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(settings.google_token_file, "w") as token:
            token.write(creds.to_json())
    return creds