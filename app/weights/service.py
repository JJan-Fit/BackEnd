from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import Member
from app.weights import repository
from app.weights.exceptions import WeightNotFound
from app.weights.models import Weight
from app.weights.schemas import WeightCreate


async def create(session: AsyncSession, member: Member, payload: WeightCreate) -> Weight:
    weight = Weight(kg=payload.kg, member_id=member.member_id)
    return await repository.add(session, weight)


async def list_for_member(session: AsyncSession, member: Member) -> Sequence[Weight]:
    return await repository.list_by_member(session, member.member_id)


async def delete(session: AsyncSession, member: Member, weight_id: int) -> None:
    weight = await repository.get_owned(session, weight_id, member.member_id)
    if weight is None:
        raise WeightNotFound()
    await repository.delete(session, weight)
