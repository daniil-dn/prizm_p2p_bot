from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


# Shared properties
class SettingsBase(BaseModel):
    id: int


class SettingsInDB(SettingsBase):
    order_wait_minutes: int
    pay_wait_time: int
    commission_percent: Decimal
    prizm_rate_diff: Decimal


class SettingsCreate(BaseModel):
    pass


class SettingsUpdate(SettingsBase):
    order_wait_minutes: Optional[int] = None
    pay_wait_time: Optional[int] = None
    commission_percent: Optional[Decimal] = None
    prizm_rate_diff: Optional[Decimal] = None
