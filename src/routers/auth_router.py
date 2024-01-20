from fastapi import APIRouter, Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
from typing import Annotated, Tuple

from src.repository.user import UserRepo
from src.models.user_dto import UserDto
from src.models.response_dto import Content 
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
from src.service.auth_service import AuthService
from src.models.response.token_response import TokenResponse


oauth_scheme = OAuth2AuthorizationCodeBearer('/oauth', '/token' )

def get_current_user(token: Annotated[UserDto, Depends(oauth_scheme)], 
                     auth_service:AuthService = Depends(AuthService)):
    result = auth_service.decode_access_token(token)
    return result

class AuthRouter:
    router = APIRouter(prefix='/v1/auth', tags=['Auth'])

    @router.post('/signup', 
                 response_model=Content[bool], 
                 responses={
                     ExceptionsEnum.UserExists.value: 
                     UserExistsExceptionScheme.to_dump()
                 })
    async def sign_up(user: UserDto, 
                      db: UserRepo = Depends(UserRepo)
                      ):
        if db.check_user_exist(user.cell_number):
            raise UserExistsException()
        db.add_user(user)
        return Content(data=True)

    @router.post('/signin', 
                 response_model=Content[TokenResponse], 
                 responses={
                     ExceptionsEnum.UserNotExsists.value:
                     UserNotExistsExceptionScheme.to_dump(),
                     ExceptionsEnum.PasswordMismatch.value:
                     PasswordMismatchExceptionScheme.to_dump()
                 })
    async def sign_in(user: UserDto, 
                      user_db: UserRepo = Depends(UserRepo), 
                      auth_service: AuthService = Depends(AuthService)
                      ):
        if not user_db.check_user_exist(user.cell_number):
            raise UserNotExistsException()
        if not user_db.check_password(user):
            raise PasswordMismatchException()

        token = auth_service.create_access_token(user) 
        return Content(data=TokenResponse(**token.model_dump()))

    @router.post('/signout', 
                 response_model=Content[bool], 
                 responses={
                     ExceptionsEnum.UnAuthorized.value:
                     UserNotExistsExceptionScheme.to_dump(),
                 })
    async def sign_out(user_and_token: Annotated[
                            Tuple[UserDto, str], Depends(get_current_user)
                        ],
                       auth_service: AuthService = Depends(AuthService),
                      ):
        _, token = user_and_token
        result = auth_service.delete_access_token(
            TokenDto(access_token=token)
        )
        
        return Content(
            data=result
        )
