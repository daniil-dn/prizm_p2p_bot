from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# Shared properties
class WalletRequestBase(BaseModel):
    id: int


class WalletInDB(WalletRequestBase):
    user_id: Optional[int]
    currency: Optional[str]
    value: Optional[str]
    updated_at: datetime
    created_at: datetime


class WalletCreate(BaseModel):
    user_id: Optional[int]
    currency: Optional[str]
    value: Optional[str]


class WalletUpdate(WalletRequestBase):
    user_id: Optional[int] = None
    currency: Optional[str] = None
    value: Optional[str] = None
