from pydantic import BaseModel, Field

class TokenResponse(BaseModel):
    access_token: str = Field('')

    class Config:
        from_attributes = True