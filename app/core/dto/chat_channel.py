from typing import Optional

from pydantic import BaseModel


class ChatChannelCreate(BaseModel):
    user_id: int
    is_bot_admin: bool = True
    id: int
    count_in_day: int
    interval: int
    interval_in_day: str
