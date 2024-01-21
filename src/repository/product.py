from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import func, text
from src.dao.product import Product
from src.repository.repo import Repo
from src.models.product_dto import ProductDto
from src.models.user_dto import UserDto
from src.utils.logger.logger import get_logger
from src.db.db import to_pydantic

_logger = get_logger(__file__)

class ProductRepo(Repo):
    def __init__(self) -> None:
        super().__init__()
        Product.metadata.create_all(self.engine)
    
    def add_product(self, product: ProductDto):
        try: 
            with self.session as session:
                rank = len(session.query(Product).where(
                    Product.expiration_date == product.expiration_date,
                    Product.user_id == product.user_id
                ).all())

                id = str(uuid4())
                session.add(
                    Product(
                        id= id,
                        **product.model_dump(exclude='id,snowflake_id'),
                        snowflake_id=product.get_snowflake_id(rank)
                    ))
        except Exception as e:
            _logger.exception(e)
            raise e
        return id
    
    def delete_product(self, product: ProductDto) -> bool:
        with self.session as session:
            rank = len(session.query(Product).where(
                    Product.expiration_date == product.expiration_date,
                    Product.user_id == product.user_id
                ).all())

            session.query(Product).filter(
                Product.id == product.id).update({
                    Product.deleted_at: datetime.utcnow(),
                    Product.snowflake_id: product.get_snowflake_id(rank)
                })
        return True
    
    def update_product(self, product: ProductDto) -> bool:
        with self.session as session:
            rank = len(session.query(Product).where(
                    Product.expiration_date == product.expiration_date,
                    Product.user_id == product.user_id
                ).all())

            _product = session.query(Product).filter(
                Product.id == product.id).first()

            if not _product:
                return False

            session.query(Product).filter(Product.id == _product.id).update({
                    **product.model_dump(exclude='id,user_id'),
                    'snowflake_id':  product.get_snowflake_id(rank)
            })
        return True
    
    def get_product(self, product_id: str) -> Optional[ProductDto]:
        with self.session as session:
            product = session.query(Product).filter(
                Product.id == product_id
            ).first()

            if not product:
                return None
            
            return ProductDto(**to_pydantic(product))
    
    def list_product(self, cursor: str, page_size: int, user:UserDto):
        with self.session as session:
            products = session.query(Product).order_by(
                Product.snowflake_id).filter(
                Product.snowflake_id > cursor,
                Product.user_id == user.id
            ).limit(page_size).all()

            return [ProductDto(**to_pydantic(product)) for product in products]
    
    def search_keyword(self, keyword: str, user:UserDto ):
        with self.session as session:
            products = session.query(Product).order_by(
                Product.snowflake_id
            ).filter(
                Product.description.like(f'%{keyword}%'),
                Product.user_id == user.id
            ).all()

            return [ProductDto(**to_pydantic(product)) for product in products]

    def search_keyword_with_cho(self, keyword: str, user:UserDto ):
        with self.session as session:
            products = session.query(
                Product,
            ).filter(
                func.fn_choSearch(Product.name).like(f'%{keyword}%'),
            ).all()

            return [ProductDto(**to_pydantic(product)) for product in products]

