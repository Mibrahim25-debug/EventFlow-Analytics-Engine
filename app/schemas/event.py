from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional

class EventCreate(BaseModel):
    user_id: int = Field(..., description="The unique ID of the user triggering the event")
    event_type: str = Field(..., description="e.g., 'product_view', 'add_to_cart', 'purchase'")
    product_id: Optional[int] = Field(None, description="The ID of the product, if applicable")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))