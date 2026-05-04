from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.shared.mixins import OwnedByMember, SoftDeleteMixin, TimestampedMixin


class Income(Base, TimestampedMixin, OwnedByMember):
    __tablename__ = "income"

    income_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    amount: Mapped[int] = mapped_column(BigInteger, nullable=False)


class IncomeCategory(Base, TimestampedMixin, SoftDeleteMixin, OwnedByMember):
    __tablename__ = "income_category"

    income_category_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    category: Mapped[str] = mapped_column(String(64), nullable=False)


class IncomeIncomeCategory(Base):
    __tablename__ = "income_income_category"

    income_income_category_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    income_category_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("income_category.income_category_id"),
        nullable=False,
        index=True,
    )
    income_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("income.income_id"),
        nullable=False,
        index=True,
    )
