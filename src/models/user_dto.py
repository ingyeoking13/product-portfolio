from pydantic import BaseModel, Field

class UserDto(BaseModel):
    id: str = Field('')
    cell_number: str = Field('')
    password: str = Field('')

    class Config:
        from_attributes = True