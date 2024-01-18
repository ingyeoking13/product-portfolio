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

    snowflake_id: str = Field('')
    user_id: str = Field('')
