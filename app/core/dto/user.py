from datetime import datetime
from typing import Optional

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
    updated_at: datetime
    created_at: datetime


class UserCreate(UserBase):
    language_code: Optional[str] = None
    username: Optional[str] = None
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    description: Optional[str] = None
    role: Optional[str] = 'user'


class UserUpdate(UserBase):
    language_code: Optional[str] = None
    username: Optional[str] = None
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    description: Optional[str] = None
