from typing import Any
from fastapi import status, HTTPException
from src.models.response import MetaContent
from pydantic import BaseModel, Field
from enum import Enum

class ExceptionsEnum(Enum):
    Default = 400
    UserNotExsists = 404
    PasswordMismatch = 401
    TokenExpired = 401
    UserExists = 409

messages = {
    ExceptionsEnum.Default: '정의 되지 않은 에러입니다.',
    ExceptionsEnum.UserNotExsists: '존재하지 않는 유저입니다.',
    ExceptionsEnum.UserExists: '유저가 존재합니다.',
    ExceptionsEnum.PasswordMismatch: '패스워드가 불일치 합니다.',
    ExceptionsEnum.TokenExpired: '토큰이 만료되었습니다.',
}

class DefaultException(Exception):
    meta: MetaContent
    data: Any

    def __init__(self, *args, **kwargs) -> None:
        self.data = None
        self.code = ExceptionsEnum.Default
        self.message = messages[ExceptionsEnum.Default]
        super().__init__(*args, **kwargs)

class DefaultExceptionScheme(BaseModel):
    meta: MetaContent = Field(
        MetaContent(
            code=ExceptionsEnum.Default,
            message=messages[ExceptionsEnum.Default]
        )
    )
    data: Any = Field(None)

    @classmethod
    def to_dump(cls):
        return {
            'description': cls.model_fields['meta'].default.message,
            'model': cls,
        }
    