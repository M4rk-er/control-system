import pytest
from httpx import AsyncClient

from src.config.db_settings import settings
from src.config.database import async_engine, Base
from src.main import app


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
