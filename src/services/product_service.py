from datetime import datetime

from fastapi import HTTPException, status

from src.data.product_data import ProductOrm, product_orm
from src.data.shift_data import shift_orm
from src.exceptions import DoesNotExistDB, DuplicateDb
from src.models.product import Product
from src.schemas.product import ProductAdd, ProductAggregate
from src.services.base import BaseService
from src.services.shift_service import shift_service


class ProductService(BaseService[Product, ProductOrm, ProductAdd, ProductAdd]):

    async def create_products(self, product_data: list[ProductAdd]) -> list[Product]:

        created_products = []
        for product in product_data:

            filters = self.__get_shift_filters(product)
            try:
                shift = await shift_orm.select_by(**filters)
            except DoesNotExistDB:
                continue

            try:
                data = {'sku': product.sku, 'shifttask_id': shift.id}
                product_id = await self.orm_model.insert(data)
                product_obj = await self.orm_model.select_by(id=product_id)
                created_products.append(product_obj)

            except DuplicateDb:
                continue

        return created_products

    async def aggregate_product(self, aggregate_data: ProductAggregate):

        product = await self.get_obj(None, sku=aggregate_data.sku)
        await shift_service.get_obj(obj_id=aggregate_data.shift_id)

        self.__validate_product_aggregation(product, aggregate_data)
        new_values = self.__get_updated_product_data()
        await self.orm_model.update(product.id, new_values)

        return {'sku': aggregate_data.sku}

    def __get_shift_filters(self, product_data: ProductAdd) -> dict:
        return product_data.model_dump(exclude={'sku'})

    def __validate_product_aggregation(
        self, product: Product | None, aggregate_data: ProductAggregate
    ):

        if (
            product
            and product.is_aggregated
            and product.shifttask_id == aggregate_data.shift_id
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'unique code already used at {product.aggregated_at}',
            )

        if product and product.is_aggregated:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='unique code is attached to another batch',
            )

    def __get_updated_product_data(self) -> dict:
        return {'aggregated_at': datetime.utcnow(), 'is_aggregated': True}


product_service: ProductService = ProductService(product_orm)
