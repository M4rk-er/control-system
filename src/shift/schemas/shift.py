from pydantic import BaseModel, Field
from datetime import date, datetime


class Shift(BaseModel):
    id: int
    status: bool
    task: str
    shift: str
    batch_number: str
    batch_date: date
    nomenclature: str
    EKN_code: str
    RC_identifier: str
    start_at: datetime
    closed_at: datetime | None


class ShiftAdd(BaseModel):
    # status: bool = Field(default=False, alias='СтатусЗакрытия')
    task: str = Field(alias='ПредставлениеЗаданияНаСмену')
    shift: str = Field(alias='Смена')
    batch_number: str = Field(alias='НомерПартии')
    batch_date: date = Field(alias='ДатаПартии')
    nomenclature: str = Field(alias='Номенклатура')
    EKN_code: str = Field(alias='КодЕКН')
    RC_identifier: str = Field(alias='ИдентификаторРЦ')
    # start_at: datetime = Field(alias='ДатаВремяНачалаСмены')
    # closed_at: datetime | None = Field(
    #     default=None, alias='ДатаВремяОкончанияСмены'
    # )

class ShiftUpdate(ShiftAdd):
    status: bool = False
    closed_at: datetime | None = None
