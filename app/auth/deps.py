from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import repository, security
from app.auth.exceptions import TokenExpired, TokenInvalid
from app.auth.models import Member
from app.db import get_db
from app.shared.exceptions import Unauthorized

_bearer = HTTPBearer(auto_error=False)


async def get_current_member(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
    session: Annotated[AsyncSession, Depends(get_db)],
) -> Member:
    if credentials is None:
        raise Unauthorized()

    try:
        payload = security.decode_token(credentials.credentials)
    except jwt.ExpiredSignatureError as exc:
        raise TokenExpired() from exc
    except jwt.PyJWTError as exc:
        raise TokenInvalid() from exc

    sub = payload.get("sub")
    if not isinstance(sub, str) or not sub.isdigit():
        raise TokenInvalid()

    member = await repository.get_by_id(session, int(sub))
    if member is None:
        raise TokenInvalid()
    return member
