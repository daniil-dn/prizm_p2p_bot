from sqlalchemy import Column, Numeric, Integer, ForeignKey, String, func, DateTime

from app.core.db.base_class import Base
from app.core.models.model_base import ModelBase


class MessageBetween(Base, ModelBase):
    id = Column(Integer, primary_key=True)

    order_id = Column(ForeignKey('order.id'), index=True)
    from_user_id = Column(ForeignKey('user.id'), index=True)
    to_user_id = Column(ForeignKey('user.id'), index=True)
    text = Column(String(4096))
    photo = Column(String(100), nullable=True)
    document = Column(String(100), nullable=True)

    created_at = Column(DateTime(timezone=True), index=True, default=func.now())