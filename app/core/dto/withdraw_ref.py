from datetime import datetime

from pydantic import BaseModel


# Shared properties
class WithdrawRefCreate(BaseModel):
    user_id: int
    summ: float