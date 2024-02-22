from fastapi import APIRouter, Depends, status, Query
from src.schemas.shift import Shift as ShiftSchema, ShiftAdd, ShiftUpdate, ShiftsFiltering
from src.services.shift_service import shift_service


shift_router = APIRouter(prefix='/shifts', tags=['Shifts'])


@shift_router.get('/', response_model=list[ShiftSchema])
async def get_all_shifts(
    offset: int = Query(0), limit: int = Query(20), filters: ShiftsFiltering = Depends()
):
    shifts = await shift_service.list(offset, limit, filters)
    return shifts

@shift_router.get('/{obj_id}/', response_model=ShiftSchema)
async def get_shift(shift = Depends(shift_service.get_obj)):
    return shift

@shift_router.post('/', response_model=ShiftSchema, status_code=status.HTTP_201_CREATED)
async def add_shift(shift_data: ShiftAdd):
    shift = await shift_service.create_obj(shift_data)
    return shift

@shift_router.patch('/{obj_id}/', response_model=ShiftSchema)
async def change_shift(obj_id: int, updated_shift: ShiftUpdate):
    shift = await shift_service.shift_update(obj_id, updated_shift)
    return shift