from src.repository.user import UserRepo
from src.dao.user import User
from src.models.user_dto import UserDto
from src.models.response import Content, MetaContent
from fastapi import APIRouter, Depends, Cookie, Response
from datetime import datetime, timedelta
from src.exceptions.user_exists import (
    UserExistsException, ExceptionsEnum, UserExistsExceptionScheme,
)
from src.exceptions.user_not_exists import (
    UserNotExistsException, UserNotExistsExceptionScheme
)
from src.exceptions.user_passwords import (
    PasswordMismatchException, PasswordMismatchExceptionScheme
)
from src.models.token_dto import TokenDto
import jwt

secret_key = 'my_secret_key' 
expire_minutes = 30

class AuthRouter:
    router = APIRouter(prefix='/v1/auth')

    @router.post('/signup', response_model=Content[bool], responses={
        ExceptionsEnum.UserExists.value: UserExistsExceptionScheme.to_dump()
    })
    async def sign_up(user: UserDto, 
                      db: UserRepo = Depends(UserRepo)
                      ):
        # 사장님은 시스템에 휴대폰번호와 비밀번호 입력을 통해서 회원 가입을 할 수 있습니다. 
        # - 사장님의 휴대폰 번호를 올바르게 입력했는지 확인해주세요
        # - 비밀번호를 안전하게 보관할 수 있는 장치를 만들어주세요
        if db.check_user_exist(user.cell_number):
            raise UserExistsException()
        db.add_user(user)
        return Content(
            data=True,
            meta=MetaContent(
                code=200, message='' 
            )
        )

    @router.post('/signin', response_model=Content[TokenDto], responses={
        ExceptionsEnum.UserNotExsists.value: 
            UserNotExistsExceptionScheme.to_dump(),
        ExceptionsEnum.PasswordMismatch.value: 
            PasswordMismatchExceptionScheme.to_dump()
    })
    async def sign_in(user: UserDto, db: UserRepo = Depends(UserRepo)):
        if not db.check_user_exist(user.cell_number):
            raise UserNotExistsException()
        if not db.check_password(user):
            raise PasswordMismatchException()
        
        return Content(
            data={
                TokenDto(access_token=jwt.encode({
                    'expire': (
                        datetime.utcnow()+timedelta(minutes=30)
                    ).isoformat()
                }, secret_key, 'HS256'))
            }
        )
