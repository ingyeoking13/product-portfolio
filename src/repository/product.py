from datetime import datetime

from src.dao.product import Product
from src.repository.repo import Repo
from src.models.product_dto import ProductDto
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

                session.add(
                    Product(
                        **product.model_dump(exclude='id,snowflake_id'),
                        snowflake_id=product.get_snowflake_id(rank)
                    ))
        except Exception as e:
            _logger.exception(e)
            raise e
        return True
    
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
    
    def get_product(self, product_id: str) -> ProductDto:
        with self.session as session:
            product = session.query(Product).filter(
                Product.id == product_id
            ).first()

            if not product:
                return False
            
            return ProductDto(**to_pydantic(product))
    
    def list_product(self, cursor: str, page_size: int ):
        with self.session as session:
            products = session.query(Product).order_by(
                Product.snowflake_id).filter(
                Product.snowflake_id > cursor
            ).limit(page_size).all()

            return [ProductDto(**to_pydantic(product)) for product in products]
