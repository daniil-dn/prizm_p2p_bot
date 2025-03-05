from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


# Shared properties
class OrderRequestBase(BaseModel):
    id: int


class OrderRequestInDB(OrderRequestBase):
    user_id: Optional[int]
    from_currency: Optional[str]
    to_currency: Optional[str]
    min_limit: Optional[Decimal]
    max_limit: Optional[Decimal]
    min_limit_rub: Optional[Decimal]
    max_limit_rub: Optional[Decimal]
    rate: Optional[Decimal]
    status: Optional[int]
    updated_at: datetime
    created_at: datetime


class OrderRequestCreate(BaseModel):
    user_id: Optional[int]
    from_currency: Optional[str]
    to_currency: Optional[str]
    min_limit: Optional[Decimal]
    max_limit: Optional[Decimal]
    min_limit_rub: Optional[Decimal]
    max_limit_rub: Optional[Decimal]
    rate: Optional[Decimal]
    status: Optional[int]


class OrderRequestUpdate(OrderRequestBase):
    min_limit: Optional[Decimal] = None
    max_limit: Optional[Decimal] = None
    min_limit_rub: Optional[Decimal]
    max_limit_rub: Optional[Decimal]
    rate: Optional[Decimal] = None
    status: Optional[int] = None
