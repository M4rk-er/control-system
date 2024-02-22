import datetime
from src.shift.models.shift import ShiftTask
from src.shift.data.shift import shift_orm, ShiftORM
from src.shift.schemas.shift import ShiftAdd, ShiftUpdate
from src.shift.services.base import BaseService


class ShiftService(BaseService[ShiftTask, ShiftORM, ShiftAdd, ShiftUpdate]):

    async def shift_update(self, obj_id: int, new_values: ShiftUpdate) -> ShiftTask | None:

        data = new_values.model_dump(exclude_unset=True)
        if 'is_closed' in data:
            data['closed_at'] = datetime.datetime.utcnow()

        await self.orm_model.update(obj_id, data)
        obj = await self.get_obj(obj_id)
        return obj

shift_service: ShiftService = ShiftService(shift_orm)
