import asyncio
import sys
from pathlib import Path

# Allow `python3 scripts/run_briefing.py` from repo root without PYTHONPATH=.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.runner import run_morning_briefing


if __name__ == "__main__":
    result = asyncio.run(run_morning_briefing())
    print(result)