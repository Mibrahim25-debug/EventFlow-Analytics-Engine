from sqlalchemy import Column, Integer, String, DateTime, Index
from datetime import datetime, timezone
from app.db.database import Base

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key= True, index=True)
    
    user_id = Column(Integer, index=True)
    event_type = Column(String, index=True)
    product_id = Column(Integer, nullable=True)
    
    timestamp = Column(DateTime, default= lambda: datetime.now(timezone.utc))
    
Index("idx_event_time", Event.event_type, Event.timestamp)