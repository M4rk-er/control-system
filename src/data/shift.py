from src.data.base import CrudBase
from src.models.shift import ShiftTask
from src.schemas.shift import ShiftAdd, ShiftUpdate


class ShiftORM(CrudBase[ShiftTask, ShiftAdd, ShiftUpdate]):
    pass


shift_orm: ShiftORM = ShiftORM(ShiftTask)
