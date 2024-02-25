import pytest
from datetime import date

from tests.utils import PRODUCT_ID, SHIFT_DATA_AMOUNT


@pytest.fixture
def product_body() -> list[dict]:
    product = [{
        'sku': 'skuintest',
        'batch_number': 456,
        'batch_date': str(date(2024, 1, 1)),
    }]
    return product


@pytest.fixture
def product_response() -> list[dict]:
    product = [{
        'id': PRODUCT_ID,
        'sku': 'skuintest',
        'is_aggregated': False,
        'aggregated_at': None,
    }]
    return product

@pytest.fixture
def aggregate_body() -> dict:
    agg = {
        'shift_id': SHIFT_DATA_AMOUNT,
        'sku': 'skuintest'
    }
    return agg

@pytest.fixture(scope='session')
def product_db() -> dict:
    product = {
        'sku': 'testdbsku',
        'shifttask_id': 1,
    }
    return product
