from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class WithdrawalInDB(BaseModel):
    id: int
    user_id: int
    amount: Decimal
    commission_percent: Decimal
    wallet: str
    status: int
    created_at: datetime


class WithdrawalCreate(BaseModel):
    user_id: int
    amount: Decimal = None
    commission_percent: Decimal = None
    wallet: str
    status: int


class WithdrawalUpdate(BaseModel):
    pass
