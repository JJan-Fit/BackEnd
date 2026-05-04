from decimal import Decimal

from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.types import BigIntPK
from app.shared.mixins import OwnedByMember, TimestampedMixin


class Weight(Base, TimestampedMixin, OwnedByMember):
    __tablename__ = "weight"

    weight_id: Mapped[int] = mapped_column(BigIntPK, primary_key=True, autoincrement=True)
    kg: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
