from datetime import date, datetime
from typing import Annotated

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base, intpk, str128
from src.models.product import Product


class ShiftTask(Base):
    __tablename__ = 'shift_task'

    id: Mapped[intpk]
    is_closed: Mapped[bool] = mapped_column(sqlalchemy.Boolean, default=False)
    task: Mapped[str128]
    work_center: Mapped[str128]
    shift: Mapped[str128]
    brigade: Mapped[str128]
    batch_number: Mapped[int] = mapped_column(sqlalchemy.Integer, unique=True)
    batch_date: Mapped[date]
    nomenclature: Mapped[str128]
    EKN_code: Mapped[str128]
    RC_identifier: Mapped[str128]
    start_at: Mapped[Annotated[datetime, mapped_column(
        default=datetime.utcnow
    )]]
    closed_at: Mapped[datetime | None]

    products: Mapped[list['Product']] = relationship(
        back_populates='shift'
    )

    __table_args__ = (
        sqlalchemy.UniqueConstraint('batch_number', 'batch_date'),
    )
