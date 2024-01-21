from typing import Any
from pydantic import Field
from src.exceptions.exceptions import (
    ExceptionsEnum, messages, DefaultException, MetaContent, 
    DefaultExceptionScheme
)

class CellNumberInvalidException(DefaultException):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.code = ExceptionsEnum.CellNumberInvalid
        self.message = messages[ExceptionsEnum.CellNumberInvalid]
    
class CellNumberInvalidExceptionScheme(DefaultExceptionScheme):
    meta: MetaContent = Field(
        MetaContent(
            code=ExceptionsEnum.CellNumberInvalid,
            message=messages[ExceptionsEnum.CellNumberInvalid]
        )
    )
    data: Any = Field(None)
