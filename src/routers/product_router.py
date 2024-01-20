from fastapi import APIRouter, Depends, Body, Response
from fastapi.security import OAuth2AuthorizationCodeBearer
from typing import Annotated, Tuple, List

from src.repository.product import ProductRepo
from src.models.user_dto import UserDto
from src.repository.user import UserRepo
from src.models.response_dto import Content 
from src.models.product_dto import ProductDto
from src.exceptions.unauthorized import (
    UnAuthorizedException, UnAuthorizedExceptionScheme, ExceptionsEnum
)
from src.exceptions.unprocessable_content import (
    UnprocessableContentException, UnprocessableContentExceptionScheme
)
from src.service.auth_service import AuthService
from src.service.product_service import ProductService


oauth_scheme = OAuth2AuthorizationCodeBearer('/oauth', '/token' )

def get_current_user(token: Annotated[UserDto, Depends(oauth_scheme)], 
                     auth_service:AuthService = Depends(AuthService)):
    result = auth_service.decode_access_token(token)
    return result

class ProductRouter:
    router = APIRouter(prefix='/v1/product', 
                        responses={
                            ExceptionsEnum.UnAuthorized.value:
                            UnAuthorizedExceptionScheme.to_dump(),
                            ExceptionsEnum.UnprocessableContent.value:
                            UnprocessableContentExceptionScheme.to_dump()
                        }
                       , tags=['Product'])

    @router.post('', response_model=Content[bool])
    async def post_product(
        product: ProductDto, 
        user_and_token: Tuple[UserDto, str] = Depends(get_current_user),
        product_service: ProductService = Depends(ProductService)
    ):
        user, _ = user_and_token
        product_service.upload_product(product, user)
        return Content(data=True)

    @router.get('/search/{id}', response_model=Content[ProductDto])
    async def get_product(
        response: Response, 
        id: str, 
        user_and_token: Tuple[UserDto, str] = Depends(get_current_user),
        product_service: ProductService = Depends(ProductService)
    ):
        user, _ = user_and_token
        result = product_service.get_product(id, user)
        return Content(data=result)
    
    @router.put('', response_model=Content[bool])
    async def put_product(
        product: ProductDto, 
        user_and_token: Tuple[UserDto, str] = Depends(get_current_user),
        product_service: ProductService = Depends(ProductService)
    ):
        user, _ = user_and_token
        result = product_service.update_product(product, user)
        return Content(data=result)
    
    @router.delete('', response_model=Content[bool])
    async def delete_product(
        id: Annotated[str, Body(embed=True)], 
        user_and_token: Tuple[UserDto, str] = Depends(get_current_user),
        product_service: ProductService = Depends(ProductService)
    ):
        user, _ = user_and_token
        result = product_service.delete_product(id, user)
        return Content(data=result)

    
    @router.get('/list', response_model=Content[List[ProductDto]])
    async def get_products(
        cursor: str = '0', 
        page_size: int = 10, 
        product_db: ProductRepo = Depends(ProductRepo)
    ):
        results = product_db.list_product(cursor, page_size)

        return Content(data=results)
    
    @router.get('/search')
    async def search_products(
        keyword: str, 
        user_and_token: Tuple[UserDto, str] = Depends(get_current_user),
        product_service: ProductService = Depends(ProductService)
    ):
        user, _ = user_and_token
        result = product_service.search_product(keyword, user)
        return Content(data=result)