from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel


# Shared properties
class UserBase(BaseModel):
    id: int


class UserInDB(UserBase):
    language_code: Optional[str] = None
    username: Optional[str] = None
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    description: Optional[str] = None
    is_wallet_activated: Optional[bool] = None
    structure_path: Optional[Any] = None
    updated_at: datetime
    created_at: datetime


class UserCreate(UserBase):
    language_code: Optional[str] = None
    username: Optional[str] = None
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    description: Optional[str] = None
    is_wallet_activated: Optional[bool] = False
    role: Optional[int] = 1
    partner_id: Optional[int] = None
    structure_path: Optional[Any] = None


class UserUpdate(UserBase):
    language_code: Optional[str] = None
    username: Optional[str] = None
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    description: Optional[str] = None
    is_wallet_activated: Optional[bool] = None
    structure_path: Optional[Any] = None
