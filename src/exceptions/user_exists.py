from typing import Any
from pydantic import Field, BaseModel
from src.exceptions.exceptions import (
    ExceptionsEnum, messages, DefaultException, MetaContent, 
    DefaultExceptionScheme
)

class UserExistsException(DefaultException):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.code = ExceptionsEnum.UserExists
        self.message = messages[ExceptionsEnum.UserExists]
    
class UserExistsExceptionScheme(DefaultExceptionScheme):
    meta: MetaContent = Field(
        MetaContent(
            code=ExceptionsEnum.UserExists,
            message=messages[ExceptionsEnum.UserExists]
        )
    )
    data: Any = Field(None)
