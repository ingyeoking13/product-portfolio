from fastapi import Depends
from src.repository.token import TokenRepo
from src.models.token_dto import TokenDto
from src.repository.user import UserRepo
from src.models.user_dto import UserDto
from src.utils.time import get_cur_time

from src.exceptions.unauthorized import UnAuthorizedException
from src.exceptions.user_exists import UserExistsException
from src.exceptions.cell_number_invalid import CellNumberInvalidException

from typing import Tuple
from datetime import datetime, timedelta
import re
import jwt

class AuthService:
    secret_key = 'my_secret_key' 
    expire_minutes = 30
    algorithm = 'HS256'

    def __init__(self, 
                 user_db: UserRepo = Depends(UserRepo),
                 token_db: TokenRepo =  Depends(TokenRepo)) -> None:
        self.user_db = user_db
        self.token_db = token_db
    
    def _validate_cell_number(self, cell_number: str):
        reg = r'[0-9]{3}-[0-9]{3,4}-[0-9]{4}'
        if re.match(reg, cell_number):
            return True
        return False
    
    def sign_up_user(self, user: UserDto):
        if self.user_db.check_user_exist(user.cell_number):
            raise UserExistsException()
        
        if not self._validate_cell_number(user.cell_number):
            raise CellNumberInvalidException()

        self.user_db.add_user(user)

    def create_access_token(self, user: UserDto) -> TokenDto:
        token = TokenDto(
                access_token=jwt.encode({
                        'expire': (
                            get_cur_time()+timedelta(minutes=30)
                        ).isoformat(),
                        'cell_number': user.cell_number
                }, self.secret_key, self.algorithm),
                user_id=self.user_db.get_user(user).id
            )

        self.token_db.add_token(token)

        return token

    def delete_access_token(self, token:TokenDto):
        self.token_db.delete_token(token)
        return True
    
    def decode_access_token(self, token: str)->Tuple[UserDto, str]:
        try:
            decoded = jwt.decode(token, key=self.secret_key, 
                                algorithms=self.algorithm)
        except Exception as e:
            raise UnAuthorizedException()

        if get_cur_time() > datetime.fromisoformat(decoded['expire']):
            raise UnAuthorizedException()

        return [UserDto(**decoded), token]