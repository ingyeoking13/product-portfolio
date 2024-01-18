import uuid
from sqlalchemy import (
    Column, String, UniqueConstraint, DateTime, ForeignKey, 
)
from sqlalchemy.orm import Mapped, Relationship
from datetime import datetime
from src.dao.user import User
from src.db.db import Base

class Token(Base):
    __tablename__ = 'token'
    id: Mapped[str] = Column(String(36), primary_key=True,
                             default=lambda: str(uuid.uuid4()))
    access_token: Mapped[str] = Column(String(300), index=True)
    created_at: Mapped[datetime] = Column(
        DateTime, default=lambda: datetime.utcnow())
    deleted_at: Mapped[datetime | None] = Column(DateTime)

    user_id: Mapped[str] = Column(ForeignKey('user.id'))

