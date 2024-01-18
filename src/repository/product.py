from datetime import datetime

from src.dao.product import Product
from src.repository.repo import Repo
from src.models.product_dto import ProductDto
from src.utils.logger.logger import get_logger

_logger = get_logger(__file__)

class ProductRepo(Repo):
    def __init__(self) -> None:
        super().__init__()
        Product.metadata.create_all(self.engine)
    
    def add_product(self, product: ProductDto):
        try: 
            with self.session as session:
                session.add(
                    Product(
                        **product.model_dump(exclude='id')
                    ))
        except Exception as e:
            _logger.exception(e)
            raise
        return True
    
    def delete_product(self, product: ProductDto) -> bool:
        with self.session as session:
            session.query(Product).filter(
                Product.id == product.id).update({
                    Product.deleted_at: datetime.utcnow()
                })
        return True
    
    def update_product(self, product: ProductDto) -> bool:
        with self.session as session:
            _product = session.query(Product).filter(
                Product.id == product.id).first()

            if not _product:
                return False

            session.query(Product).filter(Product.id == _product.id).update({
                    **product.model_dump(exclude='id,user_id')
            })
        return True
    