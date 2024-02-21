from src.shift.data.base import CrudBase
from src.shift.models.shift import ShiftTask
from src.shift.schemas.shift import ShiftAdd, ShiftUpdate

class ShiftORM(CrudBase[ShiftTask, ShiftAdd, ShiftUpdate]):
    pass

shift_orm: ShiftORM = ShiftORM(ShiftTask)
