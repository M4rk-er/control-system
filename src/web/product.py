from fastapi import APIRouter, status, Depends

from src.schemas.product import ProductSchema
from src.services.product_service import product_service
from src.models.product import Product

product_router = APIRouter(prefix='/products', tags=['Products'])


@product_router.post(
    '/', status_code=status.HTTP_201_CREATED, response_model=list[ProductSchema]
)
async def product_add(product=Depends(product_service.create_products)):
    return product
