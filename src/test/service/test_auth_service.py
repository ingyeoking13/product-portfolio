import pytest
import jwt
from datetime import datetime

from src.models.user_dto import UserDto
from src.models.token_dto import TokenDto
from src.repository.user import UserRepo
from src.repository.token import TokenRepo
from src.service.auth_service import AuthService 

def empty_construct(*s):
    pass

def get_user(self, user_id: str):
    return UserDto(id='1', cell_number='123', password='123')

def add_token(*x):
    return True

def mock_utcnow(*s):
    return datetime(1970, 1, 1, 0, 0, 0, 0)

@pytest.fixture
def mock_init(monkeypatch):
    monkeypatch.setattr(UserRepo, '__init__', empty_construct)
    monkeypatch.setattr(TokenRepo, '__init__', empty_construct)
    monkeypatch.setattr(UserRepo, 'get_user', get_user)
    monkeypatch.setattr(TokenRepo, 'add_token', add_token)
    monkeypatch.setattr('src.service.auth_service.get_cur_time', mock_utcnow)
    auth_service = AuthService(UserRepo(), TokenRepo())
    return auth_service

@pytest.fixture
def test_check_create_access_token(mock_init):
    auth_service:AuthService = mock_init

    access_token_dto = auth_service.create_access_token(
        UserDto(
            id='1',
            cell_number='123',
            password='123'
        )
    )

    assert isinstance(access_token_dto, TokenDto)
    return access_token_dto


def test_expire_access_token(mock_init, test_check_create_access_token):
    access_token_dto = test_check_create_access_token
    auth_service: AuthService = mock_init
    decoded_access_token = auth_service.decode_access_token(
        access_token_dto.access_token
    )
    user, token = decoded_access_token

    assert user.cell_number == '123'
    expire_time = datetime.fromisoformat(
        jwt.decode(token, 'my_secret_key', 'HS256' )['expire']
    )
    assert expire_time == datetime(1970, 1, 1, 0, 30)

