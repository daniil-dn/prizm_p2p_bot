from datetime import datetime
from decimal import Decimal
from typing import Optional, Any

from pydantic import BaseModel


# Shared properties
class TransactionBase(BaseModel):
    id: int


class TransactionInDB(TransactionBase):
    transaction_id: Optional[int]
    from_wallet_address: str
    to_wallet_address: str
    value: Decimal
    fee: Decimal
    order_id: Optional[int]
    order_request_id: Optional[int]
    user_id: Optional[int]
    message_text: Optional[str]
    type: Optional[str]
    extra_data: Optional[Any]
    updated_at: datetime
    created_at: datetime


class TransactionCreate(BaseModel):
    transaction_id: Optional[str]
    from_wallet_address: str
    to_wallet_address: str
    value: Decimal
    fee: Decimal
    order_id: Optional[int]
    order_request_id: Optional[int]
    user_id: Optional[int]
    message_text: Optional[str]
    type: Optional[str]
    extra_data: Optional[Any]


class TransactionUpdate(TransactionBase):
    transaction_id: Optional[int]
    from_wallet_address: Optional[str]
    to_wallet_address: Optional[str]
    value: Optional[Decimal]
    fee: Optional[Decimal]
    order_id: Optional[int]
    order_request_id: Optional[int]
    user_id: Optional[int]
    message_text: Optional[str]
    type: Optional[str]
    extra_data: Optional[Any]
