from pydantic import BaseModel, Field

class TokenDto(BaseModel):
    access_token: str = Field('')

    class Config:
        from_attributes = True