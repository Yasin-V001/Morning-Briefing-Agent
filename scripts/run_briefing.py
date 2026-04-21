import asyncio
from app.runner import run_morning_briefing


if __name__ == "__main__":
    result = asyncio.run(run_morning_briefing())
    print(result)