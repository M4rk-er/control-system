from src.services.base import BaseService
from src.models.product import Product
from src.data.product import ProductOrm, product_orm
from src.schemas.product import ProductAdd
from src.exceptions import DuplicateDb

from src.services.shift_service import shift_service


class ProductService(BaseService[Product, ProductOrm, ProductAdd, ProductAdd]):
    
    async def create_products(self, product_data: list[ProductAdd]) -> list[Product]:
        created_products = []

        for product in product_data:

            filters = self.__get_shift_filters(product)
            shift = await shift_service.get_obj(None, **filters)
            if not shift:
                continue

            try:
                data = {'sku': product.sku, 'shifttask_id': shift.id}
                product_id = await product_orm.insert(data)
                product_obj = await product_orm.select_by(id=product_id)
                created_products.append(product_obj)

            except DuplicateDb:
                pass

        return created_products


    def __get_shift_filters(self, product_data: ProductAdd) -> dict:
        return product_data.model_dump(exclude={'sku'})


product_service: ProductService = ProductService(product_orm)
