from datetime import datetime

from src.dao.product import Prdouct
from src.repository.repo import Repo
from src.models.product_dto import ProductDto
from src.utils.logger.logger import get_logger

_logger = get_logger(__file__)

class ProductRepo(Repo):
    def __init__(self) -> None:
        super().__init__()
        Prdouct.metadata.create_all(self.engine)
    
    def add_product(self, product: ProductDto):
        try: 
            with self.session as session:
                session.add(
                    Prdouct(
                        **product.model_dump(exclude='id')
                    ))
        except Exception as e:
            _logger.exception(e)
            raise
        return True
    
    def delete_product(self, product: ProductDto) -> bool:
        with self.session as session:
            session.query(Prdouct).filter(
                Prdouct.id == product.id).update({
                    Prdouct.deleted_at: datetime.utcnow()
                })
        return True
    