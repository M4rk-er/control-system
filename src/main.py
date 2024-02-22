from fastapi import FastAPI

from src.web.shift import shift_router


app = FastAPI()

app.include_router(shift_router)
