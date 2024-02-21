from fastapi import APIRouter, Depends, status
from src.shift.schemas.shift import Shift as ShiftSchema, ShiftAdd
from src.shift.services.shift_service import shift_service


shift_router = APIRouter(prefix='/shifts', tags=['Shifts'])


@shift_router.get('/', response_model=ShiftSchema)
async def get_all_shifts(shifts = Depends(shift_service.list)):
    return shifts

@shift_router.get('/{obj_id}/', response_model=ShiftSchema)
async def get_shift(shift = Depends(shift_service.get_obj)):
    return shift

@shift_router.post('/', response_model=ShiftAdd, status_code=status.HTTP_201_CREATED)
async def add_shift(shift = Depends(shift_service.create_obj)):
    return shift

@shift_router.patch('/{obj_id}/', response_model=ShiftSchema)
async def change_shift(updated_shift = Depends(shift_service.update_obj)):
    return updated_shift
