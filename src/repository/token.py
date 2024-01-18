import bcrypt
from datetime import datetime

from src.dao.token import Token
from src.repository.repo import Repo
from src.models.token_dto import TokenDto
from src.utils.logger.logger import get_logger

_logger = get_logger(__file__)

class TokenRepo(Repo):
    def __init__(self) -> None:
        super().__init__()
        Token.metadata.create_all(self.engine)
    
    def add_token(self, token: TokenDto):
        try: 
            with self.session as session:
                session.add(
                    Token(
                        access_token=token.access_token,
                        user_id=token.user_id
                    ))
        except Exception as e:
            _logger.exception(e)
            raise
        return True
    
    def delete_token(self, token: TokenDto) -> bool:
        with self.session as session:
            session.query(Token).filter(
                Token.access_token == token.access_token).update({
                    Token.deleted_at: datetime.utcnow()
                })
        return True
    