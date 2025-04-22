from datetime import datetime
from decimal import Decimal
from typing import Optional, Any

from pydantic import BaseModel


# Shared properties
class PrizmNodeIPBase(BaseModel):
    id: Optional[int] = None


class PrizmNodeIPInDB(PrizmNodeIPBase):
    name: Optional[str] = None
    ip: str
    is_active: bool
    is_priority: bool
    updated_at: datetime


class PrizmNodeIPCreate(BaseModel):
    name: Optional[str] = None
    ip: Optional[str] = None
    is_active: Optional[bool] = None
    is_priority: Optional[bool] = None


class PrizmNodeIPUpdate(PrizmNodeIPBase):
    name: Optional[str] = None
    ip: Optional[str] = None
    is_active: Optional[bool] = None
    is_priority: Optional[bool] = None
