from fastapi import status
from httpx import AsyncClient

from tests.utils import SHIFT_ID, PAGINATION_SIZE, datetimes_compare


class TestShiftTask:

    async def test_shtask_avaliable(self, client: AsyncClient):

        res = await client.get('/shifts/')
        assert res.status_code != status.HTTP_400_BAD_REQUEST
        assert res.status_code == status.HTTP_200_OK
        assert len(res.json()) == PAGINATION_SIZE

    async def test_add_shtask_without_field(
        self, client: AsyncClient, shift_without_value
    ):

        request_body, expected_response = shift_without_value
        without_value_request = await client.post(
            '/shifts/', json=request_body
        )

        assert without_value_request.status_code != status.HTTP_201_CREATED
        assert without_value_request.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert without_value_request.json() == expected_response

    async def test_add_shtask(
        self, client: AsyncClient, shift_body, shift_response
    ):

        res = await client.post('/shifts/', json=shift_body)
        start_at_exp = shift_response.pop('start_at')
        respnse_body = datetimes_compare(res.json(), start_at_exp)
        assert res.status_code != status.HTTP_400_BAD_REQUEST
        assert res.status_code != status.HTTP_422_UNPROCESSABLE_ENTITY
        assert res.status_code != status.HTTP_200_OK
        assert res.status_code == status.HTTP_201_CREATED

        assert respnse_body == shift_response

    async def test_get_shtask(self, client: AsyncClient, shift_response):

        res = await client.get(f'/shifts/{SHIFT_ID}/')
        start_at_exp = shift_response.pop('start_at')
        respnse_body = datetimes_compare(res.json(), start_at_exp)
        assert res.status_code != status.HTTP_400_BAD_REQUEST
        assert res.status_code == status.HTTP_200_OK
        assert respnse_body == shift_response

    async def test_get_unexisted_shtask(self, client: AsyncClient):

        res = await client.get(f'/shifts/{SHIFT_ID + 1}/')
        assert res.status_code != status.HTTP_200_OK
        assert res.status_code != status.HTTP_400_BAD_REQUEST
        assert res.json() == {'detail': 'There are no ShiftTask.'}

    async def test_create_already_exists_date_and_sh_number(
        self, client: AsyncClient, updated_shift_request, updated_shift_response
    ):

        res = await client.post('/shifts/', json=updated_shift_request)
        start_at_exp = updated_shift_response.pop('start_at')
        respnse_body = datetimes_compare(res.json(), start_at_exp)
        assert res.status_code != status.HTTP_400_BAD_REQUEST
        assert res.status_code == status.HTTP_201_CREATED
        assert respnse_body == updated_shift_response

    async def test_partial_update_shtask(self, client: AsyncClient):

        request_body = {'is_closed': True}
        res = await client.patch(f'/shifts/{SHIFT_ID}/', json=request_body)

        assert res.status_code != status.HTTP_400_BAD_REQUEST
        assert res.status_code != status.HTTP_422_UNPROCESSABLE_ENTITY
        assert res.status_code == status.HTTP_200_OK

        assert res.json().get('is_closed') is True
        assert res.json().get('closed_at') is not None

    async def test_pagination_and_filters(self, client: AsyncClient):

        res = await client.get('/shifts/')
        assert res.status_code == status.HTTP_200_OK
        assert len(res.json()) != SHIFT_ID
        assert len(res.json()) == PAGINATION_SIZE

        res = await client.get('/shifts/?is_closed=true')
        assert res.status_code == status.HTTP_200_OK
        assert len(res.json()) == 1
