import pytest
from typing import cast, Tuple
from datetime import datetime

from src.exceptions.unprocessable_content import UnprocessableContentException

from src.repository.product import ProductRepo
from src.repository.user import UserRepo
from src.repository.token import TokenRepo

from src.models.user_dto import UserDto
from src.models.product_dto import ProductDto
from src.models.token_dto import TokenDto

from src.service.auth_service import AuthService 
from src.service.product_service import ProductService 

def default_user():
    return UserDto(id='',
                   cell_number='123',
                   password='123')

def default_product():
    return ProductDto(id='1', 
                   category='1', 
                   price=1,
                   raw_price=1,
                   name='상품1', 
                   description= '이 상품은 맛있는 과자로, 건강에 좋은 재료만을 사용하여 만들어졌습니다. 아이들 간식이나 파티 음식으로 적합합니다.',
                   barcode='1', 
                   expiration_date=mock_utcnow(),
                   size='1')

def mock_utcnow(*s):
    return datetime(1970, 1, 1, 0, 0, 0, 0)

@pytest.fixture
def mock_init(monkeypatch):
    # using test db
    monkeypatch.setenv('db_host', 
                       'mysql+pymysql://root:adkb@localhost:3306/test_portfolio')

    auth_service = AuthService(UserRepo(), TokenRepo)
    product_service = ProductService(UserRepo(), ProductRepo())
    UserRepo().add_user(default_user())
    yield auth_service, product_service
    UserRepo().del_user(default_user())

def test_upload_product(mock_init):
    auth_service, product_service =\
        cast(Tuple[AuthService, ProductService], mock_init) 

    result = product_service.upload_product(
        default_product(),
        default_user()
    )

    assert result is not None

def test_get_product(mock_init):
    auth_service, product_service =\
        cast(Tuple[AuthService, ProductService], mock_init) 
    
    id = product_service.upload_product(
        default_product(),
        default_user()
    )

    result = product_service.get_product(id, default_user())

    assert isinstance(result, ProductDto)


def test_delete_product(mock_init):
    auth_service, product_service =\
        cast(Tuple[AuthService, ProductService], mock_init) 
    
    id = product_service.upload_product(
        default_product(),
        default_user()
    )
    result = product_service.delete_product(
        id,
        default_user()
    )

    with pytest.raises(UnprocessableContentException):
        product_service.get_product(id, default_user())

def test_search_keyword_product(mock_init):
    auth_service, product_service =\
        cast(Tuple[AuthService, ProductService], mock_init) 
    
    id = product_service.upload_product(
        default_product(),
        default_user()
    )

    result = product_service.search_product('ㅅㅍ', default_user())
    assert result[0].name == default_product().name

def test_search_keyword_product_2(mock_init):
    auth_service, product_service =\
        cast(Tuple[AuthService, ProductService], mock_init) 
    
    id = product_service.upload_product(
        default_product(),
        default_user()
    )

    result = product_service.search_product('맛있는 과자로', default_user())
    assert result[0].name == default_product().name
