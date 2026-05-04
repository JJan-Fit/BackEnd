from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.shared.mixins import SoftDeleteMixin, TimestampedMixin


class Member(Base, TimestampedMixin, SoftDeleteMixin):
    __tablename__ = "member"

    member_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    nickname: Mapped[str] = mapped_column(String(64), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
