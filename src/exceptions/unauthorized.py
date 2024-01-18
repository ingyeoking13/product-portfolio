from typing import Any
from pydantic import Field
from src.exceptions.exceptions import (
    ExceptionsEnum, messages, DefaultException, MetaContent, 
    DefaultExceptionScheme
)

class UnAuthorizedException(DefaultException):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.code = ExceptionsEnum.UnAuthorized
        self.message = messages[ExceptionsEnum.UnAuthorized]
    
class UnAuthorizedExceptionScheme(DefaultExceptionScheme):
    meta: MetaContent = Field(
        MetaContent(
            code=ExceptionsEnum.UnAuthorized,
            message=messages[ExceptionsEnum.UnAuthorized]
        )
    )
    data: Any = Field(None)
