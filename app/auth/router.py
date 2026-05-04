from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import service
from app.auth.schemas import LoginRequest, MemberRead, SignupRequest, TokenRead
from app.db import get_db
from app.shared.response import ApiResponse, ok

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/signup",
    response_model=ApiResponse[MemberRead],
    status_code=status.HTTP_201_CREATED,
)
async def signup(
    payload: SignupRequest,
    session: Annotated[AsyncSession, Depends(get_db)],
) -> ApiResponse[MemberRead]:
    member = await service.signup(session, payload)
    return ok(MemberRead.model_validate(member))


@router.post("/login", response_model=ApiResponse[TokenRead])
async def login(
    payload: LoginRequest,
    session: Annotated[AsyncSession, Depends(get_db)],
) -> ApiResponse[TokenRead]:
    token = await service.authenticate(session, str(payload.email), payload.password)
    return ok(token)
