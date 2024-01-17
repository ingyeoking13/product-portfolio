import uuid
from sqlalchemy import Column, String, UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id: Mapped[str] = Column(String(36), 
                             primary_key=True, default=lambda: str(uuid.uuid4()))
    cell_number: Mapped[str] = Column(String(64), index=True)
    password: Mapped[str] = Column(String(64))

    __table_args__ = (UniqueConstraint('id'),)

