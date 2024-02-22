from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional


class ObjId(BaseModel):
    id: int


class BaseShift(BaseModel):
    task: str
    shift: str
    brigade: str
    batch_number: int
    batch_date: date
    nomenclature: str
    EKN_code: str
    RC_identifier: str


class Shift(BaseShift, ObjId):
    is_closed: bool
    start_at: datetime
    closed_at: datetime | None


class ShiftAdd(BaseModel):
    # is_closed: bool = Field(default=False, alias='СтатусЗакрытия')
    task: str = Field(alias='ПредставлениеЗаданияНаСмену')
    work_center: str = Field(alias='РабочийЦентр')
    shift: str = Field(alias='Смена')
    brigade: str = Field(alias='Бригада')
    batch_number: int = Field(alias='НомерПартии')
    batch_date: date = Field(alias='ДатаПартии')
    nomenclature: str = Field(alias='Номенклатура')
    EKN_code: str = Field(alias='КодЕКН')
    RC_identifier: str = Field(alias='ИдентификаторРЦ')
    # start_at: datetime = Field(alias='ДатаВремяНачалаСмены')
    # closed_at: datetime | None = Field(
    #     default=None, alias='ДатаВремяОкончанияСмены'
    # )


class ShiftUpdate(BaseModel):
    is_closed: Optional[bool] = None
    task: Optional[str] = None
    shift: Optional[str] = None
    brigade: Optional[str] = None
    batch_number: Optional[int] = None
    batch_date: Optional[date] = None
    nomenclature: Optional[str] = None
    EKN_code: Optional[str] = None
    RC_identifier: Optional[str] = None


class ShiftsFiltering(BaseModel):
    is_closed: Optional[bool] = None
