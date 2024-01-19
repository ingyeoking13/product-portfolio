from fastapi import Depends

from src.models.product_dto import ProductDto
from src.repository.product import ProductRepo

from src.repository.user import UserRepo

from src.models.user_dto import UserDto
from src.exceptions.unauthorized import UnAuthorizedException
from src.exceptions.unprocessable_content import UnprocessableContentException
from src.utils.korean.korean import is_only_cho

class ProductService:

    def __init__(self, 
                 user_db: UserRepo = Depends(UserRepo),
                 product_db: ProductRepo =  Depends(ProductRepo)) -> None:
        self.user_db = user_db
        self.product_db = product_db
    
    def upload_product(self, product: ProductDto, user: UserDto):
        user_dao = self.user_db.get_user(user)
        product.user_id = user_dao.id
        result = self.product_db.add_product(product)
        if not result:
            raise UnprocessableContentException()
        return result
    
    def get_product(self, product_id: str, user: UserDto):
        user_dao = self.user_db.get_user(user)
        product = self.product_db.get_product(product_id)
        if not product:
            raise UnprocessableContentException()
        if product.user_id != user_dao.id:
            raise UnAuthorizedException()
        return product
    
    def update_product(self, product: ProductDto, user: UserDto):
        user_dao = self.user_db.get_user(user)
        product.user_id = user_dao.id
        if product.user_id != user_dao.id:
            raise UnAuthorizedException()
        result = self.product_db.update_product(product)
        return result

    def delete_product(self, id: str, user: UserDto):
        result = self.product_db.delete_product(self.get_product(id, user))
        return result
    
    def search_product(self, keyword: str, user: UserDto):
        user_dao = self.user_db.get_user(user)
        user.id = user_dao.id
        if is_only_cho(keyword):
            result = self.product_db.search_keyword_with_cho(keyword, user)
        else:
            result = self.product_db.search_keyword(keyword, user)
        return result