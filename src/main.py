from fastapi import FastAPI

from src.web.product import product_router
from src.web.shift import shift_router

app = FastAPI()

app.include_router(shift_router)
app.include_router(product_router)
