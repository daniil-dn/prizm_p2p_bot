from sqlalchemy import Column, Numeric, Integer, ForeignKey, String, func, DateTime, BigInteger
from sqlalchemy.orm import Mapped, relationship

from app.core.db.base_class import Base
from app.core.models.model_base import ModelBase


class MessageBetween(Base, ModelBase):
    id = Column(Integer, primary_key=True)

    order_id = Column(Integer, ForeignKey('order.id'), index=True)
    from_user_id = Column(BigInteger, ForeignKey('user.id'), index=True)
    to_user_id = Column(BigInteger, ForeignKey('user.id'), index=True)
    text = Column(String(4096))
    photo = Column(String(100), nullable=True)
    document = Column(String(100), nullable=True)

    created_at = Column(DateTime(timezone=True), index=True, default=func.now())

    from_user: Mapped['User'] = relationship('User', foreign_keys=[from_user_id])
    to_user: Mapped['User'] = relationship('User', foreign_keys=[to_user_id])