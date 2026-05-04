from sqlalchemy import BigInteger, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.shared.mixins import OwnedByMember, SoftDeleteMixin, TimestampedMixin


class ExercisePlan(Base, TimestampedMixin, OwnedByMember):
    __tablename__ = "exercise_plan"

    exercise_plan_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    exercise_name: Mapped[str] = mapped_column(String(128), nullable=False)


class ExerciseSet(Base, TimestampedMixin):
    """운동 세트. DDL 의 ``exercise_id`` 컬럼은 ``exercise_plan`` 을 참조하는
    의도로 해석한다 (architecture 스킬 참고). 컬럼명은 DDL 그대로 유지하되
    FK 만 명시적으로 ``exercise_plan.exercise_plan_id`` 로 건다."""

    __tablename__ = "exercise_set"

    exercise_set_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    kg: Mapped[int] = mapped_column(Integer, nullable=False)
    times: Mapped[int] = mapped_column(Integer, nullable=False)
    exercise_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("exercise_plan.exercise_plan_id"),
        nullable=False,
        index=True,
    )


class ExerciseCategory(Base, TimestampedMixin, SoftDeleteMixin):
    """대분류 (가슴/등/하체/어깨/팔). 시스템 전역 — ``member_id`` 없음."""

    __tablename__ = "exercise_category"

    exercise_category_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    category: Mapped[str] = mapped_column(String(32), nullable=False)


class ExerciseDetailCategory(Base, TimestampedMixin, SoftDeleteMixin):
    """세부 카테고리 (벤치프레스/수영). 시스템 전역."""

    __tablename__ = "exercise_detail_category"

    exercise_detail_category_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    category: Mapped[str] = mapped_column(String(64), nullable=False)
    exercise_category_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("exercise_category.exercise_category_id"),
        nullable=False,
        index=True,
    )


class ExerciseExerciseCategory(Base, TimestampedMixin):
    __tablename__ = "exercise_exercise_category"

    exercise_exercise_category_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    exercise_plan_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("exercise_plan.exercise_plan_id"),
        nullable=False,
        index=True,
    )
    exercise_category_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("exercise_category.exercise_category_id"),
        nullable=False,
        index=True,
    )
