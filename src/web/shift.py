from fastapi import APIRouter, Depends, Query, status

from src.schemas.shift import Shift as ShiftSchema
from src.schemas.shift import ShiftAdd, ShiftsFiltering, ShiftUpdate
from src.services.shift_service import shift_service

shift_router = APIRouter(prefix='/shifts', tags=['Shifts'])


@shift_router.get('/', response_model=list[ShiftSchema])
async def get_all_shifts(
    offset: int = Query(0),
    limit: int = Query(20),
    filters: ShiftsFiltering = Depends()
):
    filters_dict = filters.model_dump(exclude_none=True)
    shifts = await shift_service.list_objs(offset, limit, **filters_dict)
    return shifts


@shift_router.get('/{obj_id}/', response_model=ShiftSchema)
async def get_shift(obj_id: int):
    shift = await shift_service.get_obj(obj_id)
    return shift


@shift_router.post(
    '/',
    response_model=ShiftSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_shift(shift_data: ShiftAdd):
    shift = await shift_service.create_obj(shift_data)
    return shift


@shift_router.patch('/{obj_id}/', response_model=ShiftSchema)
async def change_shift(obj_id: int, updated_shift: ShiftUpdate):
    shift = await shift_service.shift_update(obj_id, updated_shift)
    return shift
