from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class OrderRequestInDB(BaseModel):
    id: int
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
    wallet_type: Optional[int]


class OrderRequestUpdate(BaseModel):
    min_limit: Optional[Decimal] = None
    max_limit: Optional[Decimal] = None
    min_limit_rub: Optional[Decimal] = None
    max_limit_rub: Optional[Decimal] = None
    rate: Optional[Decimal] = None
    status: Optional[int] = None
    wallet_type: Optional[int] = None
