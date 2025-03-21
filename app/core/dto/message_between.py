from typing import Optional

from pydantic import BaseModel


class MessageCreate(BaseModel):
    order_id: int
    from_user_id: int
    to_user_id: int
    text: str | None = None
    photo: str | None = None
    document: str | None = None
