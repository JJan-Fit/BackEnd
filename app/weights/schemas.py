from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class WeightCreate(BaseModel):
    kg: Decimal = Field(gt=Decimal("0"), le=Decimal("999.99"), max_digits=5, decimal_places=2)


class WeightRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    weight_id: int
    kg: Decimal
    created_at: datetime
