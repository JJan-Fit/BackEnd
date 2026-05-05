from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.deps import get_current_member
from app.auth.models import Member
from app.db import get_db
from app.shared.response import ApiResponse, ok
from app.weights import service
from app.weights.schemas import WeightCreate, WeightRead

router = APIRouter(prefix="/weights", tags=["weights"])


@router.post(
    "",
    response_model=ApiResponse[WeightRead],
    status_code=status.HTTP_201_CREATED,
)
async def create_weight(
    payload: WeightCreate,
    member: Annotated[Member, Depends(get_current_member)],
    session: Annotated[AsyncSession, Depends(get_db)],
) -> ApiResponse[WeightRead]:
    weight = await service.create(session, member, payload)
    return ok(WeightRead.model_validate(weight))


@router.get("", response_model=ApiResponse[list[WeightRead]])
async def list_weights(
    member: Annotated[Member, Depends(get_current_member)],
    session: Annotated[AsyncSession, Depends(get_db)],
) -> ApiResponse[list[WeightRead]]:
    weights = await service.list_for_member(session, member)
    return ok([WeightRead.model_validate(w) for w in weights])


@router.delete("/{weight_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_weight(
    weight_id: int,
    member: Annotated[Member, Depends(get_current_member)],
    session: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    await service.delete(session, member, weight_id)
