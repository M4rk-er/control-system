import pytest
from httpx import AsyncClient
from sqlalchemy import insert

from src.config.database import Base, async_engine, execute
from src.config.db_settings import settings
from src.main import app
from src.models.shift import ShiftTask
from src.models.product import Product

from tests.utils import SHIFT_DATA_AMOUNT
from tests.utils import PRODUCT_DATA_AMOUNT
from tests.utils import generate_data_with_nums

pytest_plugins = [
    'tests.fixtures.products',
    'tests.fixtures.shifts',
]

@pytest.fixture(autouse=True, scope='session')
async def init_db():
    assert settings.MODE == 'TEST'
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url='http://testserver') as client:
        yield client


@pytest.fixture(scope='session', autouse=True)
async def shifts(init_db, shift_db):
    data = generate_data_with_nums(shift_db, SHIFT_DATA_AMOUNT)
    query = insert(ShiftTask).values(data)
    await execute(query)


@pytest.fixture(scope='session', autouse=True)
async def products(init_db, shifts, product_db):
    data = generate_data_with_nums(product_db, PRODUCT_DATA_AMOUNT)
    query = insert(Product).values(data)
    await execute(query)
