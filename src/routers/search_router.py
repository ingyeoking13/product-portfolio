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
from src.service.search_service import SearchService
from src.exceptions.unprocessable_content import (
    UnprocessableContentException, UnprocessableContentExceptionScheme
)
from src.service.auth_service import AuthService
from src.service.product_service import ProductService


class SearchRouter:
    router = APIRouter(prefix='/v1/internal/search', tags=['Search'])

    @router.post('/build', response_model=Content[bool])
    async def post_product(
        search_service: SearchService = Depends(SearchService)
    ):
        search_service.insert_to_elastic()
        return Content(data=True)

    @router.get('', response_model=Content[List[ProductDto]])
    async def post_product(
        keyword: str,
        search_service: SearchService = Depends(SearchService)
    ):
        results = search_service.search(keyword)
        return Content(data=results)