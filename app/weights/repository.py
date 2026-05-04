from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.weights.models import Weight


async def add(session: AsyncSession, weight: Weight) -> Weight:
    session.add(weight)
    await session.commit()
    await session.refresh(weight)
    return weight


async def list_by_member(session: AsyncSession, member_id: int) -> Sequence[Weight]:
    stmt = (
        select(Weight)
        .where(Weight.member_id == member_id)
        .order_by(Weight.created_at.desc(), Weight.weight_id.desc())
    )
    return (await session.execute(stmt)).scalars().all()


async def get_owned(session: AsyncSession, weight_id: int, member_id: int) -> Weight | None:
    stmt = select(Weight).where(
        Weight.weight_id == weight_id,
        Weight.member_id == member_id,
    )
    return (await session.execute(stmt)).scalar_one_or_none()


async def delete(session: AsyncSession, weight: Weight) -> None:
    await session.delete(weight)
    await session.commit()
