from typing import Any
from pydantic import Field
from src.exceptions.exceptions import (
    ExceptionsEnum, messages, DefaultException, MetaContent, 
    DefaultExceptionScheme
)

class NoContentException(DefaultException):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.code = ExceptionsEnum.NoContent
        self.message = messages[ExceptionsEnum.NoContent]
    
class NoContentExceptionScheme(DefaultExceptionScheme):
    meta: MetaContent = Field(
        MetaContent(
            code=ExceptionsEnum.NoContent,
            message=messages[ExceptionsEnum.NoContent]
        )
    )
    data: Any = Field(None)
