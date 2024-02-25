import pytest

from fastapi import status
from httpx import AsyncClient
from datetime import datetime, timedelta
from tests.utils import get_aggregate_errors_params, get_invalid_product_params


class TestProduct:

    @pytest.mark.parametrize(
        'request_body, expected_code, expected_response', 
        get_invalid_product_params(),
    )
    async def test_invalid_product_create(
        self, client: AsyncClient, request_body, expected_code, expected_response
    ):

        res = await client.post('/products/', json=request_body)
        assert res.status_code == expected_code
        assert res.json() == expected_response

    async def test_valid_product_create(self, client: AsyncClient, product_body, product_response):

        res = await client.post('/products/', json=product_body)
        assert res.status_code != status.HTTP_422_UNPROCESSABLE_ENTITY
        assert res.status_code == status.HTTP_201_CREATED
        assert res.json() == product_response

    async def test_aggregate_product(self, client: AsyncClient, aggregate_body):

        res = await client.post('/products/aggregate/', json=aggregate_body)
        assert res.status_code != status.HTTP_400_BAD_REQUEST
        assert res.status_code == status.HTTP_200_OK
        assert res.json() == {'sku': aggregate_body.get('sku')}

    @pytest.mark.parametrize(
        'request_body, expected_code, expected_response', 
        get_aggregate_errors_params(),
    )
    async def test_aggregate_errors(
        self, client: AsyncClient, request_body, expected_code, expected_response
    ):

        await client.post('/products/aggregate/', json={'sku': 'testdbsku0', 'shift_id': 2})

        res = await client.post('/products/aggregate/', json=request_body)
        assert res.status_code == expected_code
        
        detail = res.json().get('detail')
        if detail.startswith('unique code already'):
            msg, time = detail.split('at ')
            # assert time == pytest.approx(datetime.utcnow(), abs=timedelta(milliseconds=999999))
            assert msg == expected_response.get('detail')
        else:
            assert res.json() == expected_response

