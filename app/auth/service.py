from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import repository, security
from app.auth.exceptions import EmailAlreadyTaken, InvalidCredentials
from app.auth.models import Member
from app.auth.schemas import SignupRequest, TokenRead
from app.core.config import settings


async def signup(session: AsyncSession, payload: SignupRequest) -> Member:
    email = str(payload.email).lower()
    if await repository.get_by_email(session, email) is not None:
        raise EmailAlreadyTaken()
    member = Member(
        email=email,
        nickname=payload.nickname,
        password=security.hash_password(payload.password),
    )
    return await repository.add(session, member)


async def authenticate(session: AsyncSession, email: str, password: str) -> TokenRead:
    member = await repository.get_by_email(session, email.lower())
    if member is None or not security.verify_password(password, member.password):
        raise InvalidCredentials()
    access_token = security.create_access_token(subject=str(member.member_id))
    return TokenRead(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.jwt_expire_minutes * 60,
    )
