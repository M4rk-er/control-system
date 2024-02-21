from src.shift.models.shift import ShiftTask
from src.shift.data.shift import shift_orm, ShiftORM
from src.shift.schemas.shift import ShiftAdd, ShiftUpdate
from src.shift.services.base import BaseService


class ShiftService(BaseService[ShiftTask, ShiftORM, ShiftAdd, ShiftUpdate]):
    pass


shift_service: ShiftService = ShiftService(shift_orm)
