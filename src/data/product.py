from src.data.base import CrudBase

from src.models.product import Product
from src.schemas.product import ProductAdd


class ProductOrm(CrudBase[Product, ProductAdd, ProductAdd]):
    pass      


product_orm: ProductOrm = ProductOrm(Product)
