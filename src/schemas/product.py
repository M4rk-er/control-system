from pydantic import BaseModel, ConfigDict

from datetime import date


class ProductAdd(BaseModel):
    sku: str
    batch_number: int
    batch_date: date


class ProductSchema(BaseModel):
    id: int
    sku: str
    is_aggregated: bool
    aggregated_at: bool | None
