from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import Member


async def get_by_email(session: AsyncSession, email: str) -> Member | None:
    stmt = select(Member).where(Member.email == email, Member.deleted_at.is_(None))
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_by_id(session: AsyncSession, member_id: int) -> Member | None:
    stmt = select(Member).where(
        Member.member_id == member_id,
        Member.deleted_at.is_(None),
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def add(session: AsyncSession, member: Member) -> Member:
    session.add(member)
    await session.commit()
    await session.refresh(member)
    return member
