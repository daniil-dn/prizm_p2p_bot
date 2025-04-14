from sqlalchemy import Column, Numeric, Integer, ForeignKey, String, func, DateTime, BigInteger
from sqlalchemy.orm import Mapped, relationship

from app.core.db.base_class import Base
from app.core.models.model_base import ModelBase


class ChatChannel(Base, ModelBase):
    id = Column(Integer, primary_key=True)

    chat_channel_id = Column(BigInteger, nullable=True)
    is_bot_admin = Column(Integer, default=False)
    user_id = Column(BigInteger, ForeignKey('user.id'))
    count_in_day = Column(Integer)
    interval_in_day = Column(String)
    interval = Column(Integer)

    created_at = Column(DateTime(timezone=True), index=True, default=func.now())

    user: Mapped['User'] = relationship('User', foreign_keys=[user_id])