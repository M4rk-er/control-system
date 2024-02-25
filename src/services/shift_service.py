import datetime

from src.data.shift import ShiftORM, shift_orm
from src.models.shift import ShiftTask
from src.schemas.shift import ShiftAdd, ShiftUpdate
from src.services.base import BaseService
from src.exceptions import DoesNotExistDB


class ShiftService(BaseService[ShiftTask, ShiftORM, ShiftAdd, ShiftUpdate]):

    async def shifts_create(self, shift: ShiftAdd) -> ShiftTask | None:
        
        try:
            is_shift = await self.orm_model.select_by(
                batch_number=shift.batch_number,
                batch_date=shift.batch_date,
            )
            shift_obj = await self.shift_update(
                obj_id=is_shift.id, new_values=shift
            )

        except DoesNotExistDB:
            shift_id = await self.orm_model.insert(shift.model_dump())
            shift_obj = await self.orm_model.select_by(id=shift_id)
           
        return shift_obj


    async def shift_update(
        self, obj_id: int, new_values: ShiftUpdate | ShiftAdd
    ) -> ShiftTask | None:

        data = new_values.model_dump(exclude_unset=True)
        if 'is_closed' in data:
            data['closed_at'] = datetime.datetime.utcnow()

        await self.orm_model.update(obj_id, data)
        obj = await self.get_obj(obj_id)
        return obj


shift_service: ShiftService = ShiftService(shift_orm)
