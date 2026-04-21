from app.config import settings
from app.utils.logging_utils import get_logger

logger = get_logger(__name__)


async def deliver_briefing(message: str) -> bool:
    mode = settings.openclaw_delivery_mode.lower()

    if mode == "stdout":
        print("\n===== MORNING BRIEFING =====")
        print(message)
        print("============================\n")
        logger.info("Delivered briefing via stdout.")
        return True

    logger.warning("OpenClaw delivery mode is not configured yet.")
    return False