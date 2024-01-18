from typing import Any
from pydantic import Field
from src.exceptions.exceptions import (
    ExceptionsEnum, messages, DefaultException, MetaContent, 
    DefaultExceptionScheme
)

class UnprocessableContentException(DefaultException):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.code = ExceptionsEnum.UnprocessableContent
        self.message = messages[ExceptionsEnum.UnprocessableContent]
    
class UnprocessableContentExceptionScheme(DefaultExceptionScheme):
    meta: MetaContent = Field(
        MetaContent(
            code=ExceptionsEnum.UnprocessableContent,
            message=messages[ExceptionsEnum.UnprocessableContent]
        )
    )
    data: Any = Field(None)
