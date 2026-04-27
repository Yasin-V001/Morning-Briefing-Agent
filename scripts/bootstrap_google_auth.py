import sys
from pathlib import Path
import argparse
import os

from google_auth_oauthlib.flow import InstalledAppFlow

# Allow running this script directly from the repository root.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import settings

SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/gmail.readonly",
]


def _run_manual_flow(flow: InstalledAppFlow):
    # Google requires redirect_uri in the auth request; keep it aligned with our local callback.
    # OAuth over localhost is HTTP, so oauthlib needs this flag for local development.
    os.environ.setdefault("OAUTHLIB_INSECURE_TRANSPORT", "1")
    flow.redirect_uri = "http://localhost:8088"
    auth_url, _ = flow.authorization_url(
        access_type="offline",
        prompt="consent",
    )
    print("Open this URL in one browser tab and finish login:")
    print(auth_url)
    print(
        "\nAfter Google redirects, copy the full final URL from your browser address bar\n"
        "and paste it below."
    )
    redirected_url = input("Redirected URL: ").strip()
    flow.fetch_token(authorization_response=redirected_url)
    return flow.credentials


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manual",
        action="store_true",
        help="Use manual OAuth flow (best for SSH/headless servers).",
    )
    args = parser.parse_args()

    flow = InstalledAppFlow.from_client_secrets_file(
        settings.google_client_secret_file,
        SCOPES,
    )
    if args.manual:
        creds = _run_manual_flow(flow)
    else:
        creds = flow.run_local_server(
            port=8088,
            prompt ="consent",
            access_type="offline",
        )

    with open(settings.google_token_file, "w") as token:
        token.write(creds.to_json())
    print(f"Saved token to {settings.google_token_file}")


if __name__ == "__main__":
    main()