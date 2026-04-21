from fastapi import FastAPI
from app.runner import run_morning_briefing

app = FastAPI(title="Morning Briefing Agent")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/run")
async def run():
    briefing = await run_morning_briefing()
    return {"success": True, "briefing": briefing}