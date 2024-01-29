import os
import sys
from pathlib import Path

# Add the parent directory to sys.path
parent_dir = str(Path(__file__).resolve().parent.parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

print(sys.path)

from src.utils.yaml.settings import load_settings
from src.repository.product import ProductRepo
from src.models.product_dto import ProductDto
from src.dao.product import Product

from src.dao.user import User

from faker import Faker, providers
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session
from typing import cast
from datetime import datetime
import random


fake = Faker('ko_KR')

cnt : int = 0

def snowflake_id(obj: dict):
    return ( '0-' +
             str(
                 int(cast(datetime, obj['expiration_date']).timestamp())
                 ).zfill(20) +
            '-' +
            str(cnt).zfill(10)
        )

def generate_fake_product():
    g= {
        'category': random.choice(['Food', 'Cofee']),
        'price': fake.random_int(min=10000, max=80000),
        'raw_price': fake.random_int(min=10000, max=40000),
        'name':fake.name(),
        'description':fake.text(),
        'barcode': fake.ean(length=13),
        'expiration_date': fake.date_time(),
        'size': fake.random_int(min=1, max=13),
        'user_id': 'b2c3d4e5-f6g7-8901-h2i3-j4k5l6m7n8o9', ## replaced
    }
    global cnt 
    cnt += 1
    g['snowflake_id'] = snowflake_id(g)
    return g

if __name__ == '__main__':
    engine : Engine = create_engine(
        **load_settings()['db']
    )

    session = Session(engine)
    for i in range(100000):
        session.add(Product(**generate_fake_product()))
        session.commit()

