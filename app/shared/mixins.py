from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column


class TimestampedMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


class SoftDeleteMixin:
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )


class OwnedByMember:
    member_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("member.member_id"),
        nullable=False,
        index=True,
    )
