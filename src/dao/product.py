import uuid
from sqlalchemy import (
    Column, String, ForeignKey, 
    Float, Text, DateTime
)
from sqlalchemy.orm import Mapped
from datetime import datetime
from src.db.db import Base

class Product(Base):
    __tablename__ = 'product'
    id: Mapped[str] = Column(String(36), primary_key=True,
                             default=lambda: str(uuid.uuid4()))
    category: Mapped[str] = Column(String(36), index=True, comment='카테고리')
    price: Mapped[float] = Column(
        Float, default=lambda: datetime.utcnow(), comment='가격')
    raw_price: Mapped[float] = Column(Float, comment='원가')
    name: Mapped[str] = Column(String(36), comment='이름')
    description: Mapped[str] = Column(Text, comment='설명')
    barcode: Mapped[str] = Column(Text, comment='바코드')
    expiration_date: Mapped[datetime] = Column(DateTime, comment='유통기한')
    size: Mapped[str] = Column(String(36), comment='사이즈')
    snowflake_id: Mapped[str] = Column(String(100), 
                                       comment='스노우플레이크 ID/커서용')
    deleted_at: Mapped[datetime | None] = Column(DateTime)

    user_id: Mapped[str] = Column(ForeignKey('user.id'))
