from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.types import BigIntPK
from app.shared.mixins import OwnedByMember, SoftDeleteMixin, TimestampedMixin


class Expend(Base, TimestampedMixin, OwnedByMember):
    """지출. ``category`` 는 ``expend_category`` 가 soft-delete 돼도
    이름이 보존되도록 생성 시점에 박제하는 스냅샷 컬럼이다."""

    __tablename__ = "expend"

    expend_id: Mapped[int] = mapped_column(BigIntPK, primary_key=True, autoincrement=True)
    amount: Mapped[int] = mapped_column(BigInteger, nullable=False)
    category: Mapped[str] = mapped_column(String(64), nullable=False)


class ExpendCategory(Base, TimestampedMixin, SoftDeleteMixin, OwnedByMember):
    __tablename__ = "expend_category"

    expend_category_id: Mapped[int] = mapped_column(BigIntPK, primary_key=True, autoincrement=True)
    category: Mapped[str] = mapped_column(String(64), nullable=False)


class ExpendExpendCategory(Base):
    __tablename__ = "expend_expend_category"

    expend_expend_category_id: Mapped[int] = mapped_column(
        BigIntPK, primary_key=True, autoincrement=True
    )
    expend_category_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("expend_category.expend_category_id"),
        nullable=False,
        index=True,
    )
    expend_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("expend.expend_id"),
        nullable=False,
        index=True,
    )
