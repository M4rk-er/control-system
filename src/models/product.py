from datetime import datetime

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base, intpk


class Product(Base):
    __tablename__ = "shift_product"

    id: Mapped[intpk]
    sku: Mapped[str] = mapped_column(sqlalchemy.String(128), unique=True)
    is_aggregated: Mapped[bool] = mapped_column(sqlalchemy.Boolean, default=False)
    aggregated_at: Mapped[datetime] = mapped_column(
        sqlalchemy.DateTime, nullable=True
    )
    shifttask_id: Mapped[int] = mapped_column(
        sqlalchemy.ForeignKey("shift_task.id", ondelete="CASCADE"), nullable=True
    )

    shift: Mapped["ShiftTask"] = relationship(back_populates="products")
