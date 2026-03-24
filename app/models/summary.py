from sqlalchemy import Column, Integer, Float, DateTime
from app.db.database import Base
from datetime import datetime, timezone

class DashboardSummary(Base):
    __tablename__ = "dashboard_summaries"

    id = Column(Integer, primary_key=True, index=True)
    
    # When did the background job run?
    calculated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # The pre-calculated answers
    total_events = Column(Integer)
    conversion_rate = Column(Float)
    top_product_id = Column(Integer, nullable=True)