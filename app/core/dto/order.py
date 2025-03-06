from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


# Shared properties
class OrderBase(BaseModel):
    id: int


class OrderInDB(OrderBase):
    from_user_id: Optional[int]
    to_user_id: Optional[int]
    from_currency: Optional[str]
    to_currency: Optional[str]
    status: Optional[int]
    mode: Optional[str]
    prizm_value: Optional[Decimal]
    rub_value: Optional[Decimal]
    commission_percent: Optional[Decimal]
    order_request_id: Optional[int]
    updated_at: datetime
    created_at: datetime


class OrderCreate(BaseModel):
    from_user_id: Optional[int]
    to_user_id: Optional[int]
    from_currency: Optional[str]
    to_currency: Optional[str]
    prizm_value: Optional[Decimal]
    rub_value: Optional[Decimal]
    commission_percent: Optional[Decimal]
    status: Optional[int]
    mode: Optional[str]
    order_request_id: int


class OrderUpdate(OrderBase):
    min_limit: Optional[Decimal] = None
    max_limit: Optional[Decimal] = None
    rate: Optional[Decimal] = None
    status: Optional[int] = None
    mode: Optional[str] = None
    prizm_value: Optional[Decimal] = None
    rub_value: Optional[Decimal] = None
    comm11ission_percent: Optional[Decimal] = None
    order_request_id: Optional[int]
