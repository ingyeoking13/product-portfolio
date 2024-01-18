from typing import Any
from pydantic import Field, BaseModel
from src.exceptions.exceptions import (
    ExceptionsEnum, messages, DefaultException, MetaContent, 
    DefaultExceptionScheme
)

class UserNotExistsException(DefaultException):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.code = ExceptionsEnum.UserNotExsists
        self.message = messages[ExceptionsEnum.UserNotExsists]
    
class UserNotExistsExceptionScheme(DefaultExceptionScheme):
    meta: MetaContent = Field(
        MetaContent(
            code=ExceptionsEnum.UserNotExsists,
            message=messages[ExceptionsEnum.UserNotExsists]
        )
    )
    data: Any = Field(None)
