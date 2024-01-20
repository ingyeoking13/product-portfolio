import bcrypt

from src.dao.user import User
from src.repository.repo import Repo
from src.models.user_dto import UserDto
from src.db.db import to_pydantic
from src.utils.logger.logger import get_logger

_logger = get_logger(__file__)

class UserRepo(Repo):
    def __init__(self) -> None:
        super().__init__()
        User.metadata.create_all(self.engine)
    
    def add_user(self, user: UserDto):
        try: 
            salt = bcrypt.gensalt()
            with self.session as session:
                session.add(User(cell_number=user.cell_number,
                    password=bcrypt.hashpw(
                        user.password.encode('utf-8'),
                        salt)
                    ))
        except Exception as e:
            _logger.exception(e)
            raise e
        return True
    
    def del_user(self, user: UserDto):
        try:
            with self.session as session:
                session.query(User).filter(
                    User.cell_number == user.cell_number).delete()
        except Exception as e:
            _logger.exception(e)
            raise e
        return True
    
    def check_user_exist(self, cell_number: str) -> bool:
        with self.session as session:
            result = session.query(User).filter(
                User.cell_number == cell_number).first()
        return result
    
    def check_password(self, user: UserDto) -> bool:
        with self.session as session:
            result = session.query(User).filter(
                User.cell_number == user.cell_number).first()
            return bcrypt.checkpw(
                user.password.encode('utf-8'),
                result.password.encode('utf-8')
            )
    
    def get_user(self, user: UserDto) -> UserDto:
        with self.session as session:
            result = session.query(User).filter(
                User.cell_number == user.cell_number).first()
            
            return UserDto(**to_pydantic(result))
