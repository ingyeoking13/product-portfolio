from typing import Optional 
from pydantic import BaseModel, Field
from datetime import datetime

class ProductDto(BaseModel):
    id: str = Field('') 

    category: str 
    price: float 
    raw_price: float 
    name: str 
    description: str 
    barcode: str
    expiration_date: datetime
    size: str

    deleted_at: Optional[datetime] = Field(None)
    snowflake_id: str = Field('')
    user_id: str = Field('')

    def get_snowflake_id(self,rank: int):
        return (
                ('1' if not self.deleted_at else '0') +
                '-' +
                str(int(self.expiration_date.timestamp())).zfill(20) +
                '-' +
                str(rank).zfill(10)
            )
