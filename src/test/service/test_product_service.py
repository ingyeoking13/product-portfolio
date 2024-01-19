import pytest
from typing import cast, Tuple
import jwt
from datetime import datetime

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
                   name='1',
                   description='123',
                   barcode='1', 
                   expiration_date=mock_utcnow(),
                   size='1'),

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

        default_user()
    )

    assert result == True
