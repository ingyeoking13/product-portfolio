from contextlib import contextmanager
from typing import Generator
import bcrypt

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session
from src.utils.yaml.settings import load_settings
from src.utils.logger.logger import get_logger

_logger = get_logger(__file__)

class Repo:
    def __init__(self) -> None:
        self.engine: Engine = create_engine(
            **load_settings()['db']
        )
    
    @property
    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        session = Session(self.engine)
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()