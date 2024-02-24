from datetime import date

from pydantic import BaseModel


class ProductAdd(BaseModel):
    sku: str
    batch_number: int
    batch_date: date


class ProductSchema(BaseModel):
    id: int
    sku: str
    is_aggregated: bool
    aggregated_at: bool | None


class ProductAggregate(BaseModel):
    shift_id: int
    sku: str
