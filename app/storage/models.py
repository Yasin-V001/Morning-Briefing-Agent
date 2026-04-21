from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime
from datetime import datetime
from app.storage.db import Base


class BriefingRun(Base):
    __tablename__ = "briefing_runs"

    id = Column(Integer, primary_key=True, index=True)
    run_date = Column(String, index=True, nullable=False)
    status = Column(String, nullable=False)
    briefing_text = Column(Text, nullable=True)
    delivered = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)