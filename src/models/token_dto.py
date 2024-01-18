from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TokenDto(BaseModel):
    access_token: str = Field('')
    created_at: Optional[datetime] = Field(None)
    deleted_at: Optional[datetime] = Field(None)
    user_id: Optional[str] = Field('')

    class Config:
        from_attributes = True