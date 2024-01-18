from typing import Any
from pydantic import Field, BaseModel
from src.exceptions.exceptions import (
    ExceptionsEnum, messages, DefaultException, MetaContent, 
    DefaultExceptionScheme
)

class PasswordMismatchException(DefaultException):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.code = ExceptionsEnum.PasswordMismatch
        self.message = messages[ExceptionsEnum.PasswordMismatch]
    
class PasswordMismatchExceptionScheme(DefaultExceptionScheme):
    meta: MetaContent = Field(
        MetaContent(
            code=ExceptionsEnum.PasswordMismatch,
            message=messages[ExceptionsEnum.PasswordMismatch]
        )
    )
    data: Any = Field(None)
