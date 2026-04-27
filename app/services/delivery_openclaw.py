import subprocess
from app.config import settings
from app.utils.logging_utils import get_logger

logger = get_logger(__name__)


async def deliver_briefing(message: str) -> bool:
    logger.info(
        "OpenClaw config: enabled=%s mode=%s recipient=%s",
        settings.openclaw_enabled,
        settings.openclaw_delivery_mode,
        settings.openclaw_recipient,
    )

    if not settings.openclaw_enabled:
        print(message)
        logger.warning("OpenClaw disabled. Printed to stdout only.")
        return False

    mode = settings.openclaw_delivery_mode.lower().strip()

    if mode == "telegram":
        cmd = [
            "openclaw",
            "message",
            "send",
            "--channel",
            "telegram",
            "--target",
            settings.openclaw_recipient,
            "--message",
            message,
        ]
    elif mode == "voicecall":
        cmd = [
            "openclaw",
            "voicecall",
            "call",
            "--to",
            settings.openclaw_recipient,
            "--message",
            message,
        ]
    else:
        print(message)
        logger.error("Unsupported OpenClaw delivery mode: %s", mode)
        return False

    logger.info("Running OpenClaw command: %s", " ".join(cmd[:7]) + " ...")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )

    logger.info("OpenClaw stdout: %s", result.stdout)
    logger.info("OpenClaw stderr: %s", result.stderr)

    if result.returncode != 0:
        logger.error("OpenClaw delivery failed with code %s", result.returncode)
        return False

    logger.info("Delivered briefing via OpenClaw Telegram.")
    return True