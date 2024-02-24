from httpx import AsyncClient
from fastapi import status

class TestShiftTask:

    async def test_shifts_avaliable(self, client: AsyncClient):
        
        res = await client.get('shifts/')
        assert res.status_code != status.HTTP_400_BAD_REQUEST
        assert res.status_code == status.HTTP_200_OK
