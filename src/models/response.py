from pydantic import BaseModel, Field
from typing import cast

class MetaContent(BaseModel):
    code: int = Field(200)
    message: str = Field('')

class Content[T](BaseModel):
    data: T
    meta: MetaContent