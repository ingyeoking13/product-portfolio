from fastapi import APIRouter, Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
from typing import Annotated, Tuple

from src.repository.product import ProductRepo
from src.models.user_dto import UserDto
from src.repository.user import UserRepo
from src.models.response_dto import Content 
from src.models.product_dto import ProductDto
from src.exceptions.user_exists import (
    UserExistsException, ExceptionsEnum, UserExistsExceptionScheme,
)
from src.service.auth_service import AuthService


oauth_scheme = OAuth2AuthorizationCodeBearer('/oauth', '/token' )

def get_current_user(token: Annotated[UserDto, Depends(oauth_scheme)], 
                     auth_service:AuthService = Depends(AuthService)):
    result = auth_service.decode_access_token(token)
    return result

class ProductRouter:
    router = APIRouter(prefix='/v1/product')

    @router.post('', response_model=Content[bool], responses={
        ExceptionsEnum.UnprocessableContent.value: 
            UserExistsExceptionScheme.to_dump()
    })
    async def post_product(product: ProductDto, 
                           user_and_token: Tuple[UserDto, str] =
                            Depends(get_current_user),
                           product_db: ProductRepo = Depends(ProductRepo),
                           user_db: UserRepo = Depends(UserRepo)
                           ):
        user, _ = user_and_token
        user_dao = user_db.get_user(user)
        product.user_id = user_dao.id
        product_db.add_product(product)

        return Content(data=True)
    