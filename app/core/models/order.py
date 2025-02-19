from sqlalchemy import Column, DateTime, BigInteger, func, ForeignKey, Index, String, SmallInteger

from sqlalchemy.orm import relationship, Mapped

from app.core.db.base_class import Base
from app.core.models.model_base import ModelBase
from app.core.models.user import User


class Order(Base, ModelBase):
    __table_args__ = (
        Index('ix_seller_buyer', "from_user_id", "to_user_id"),
    )

    id = Column(BigInteger, primary_key=True)
    from_user_id = Column(ForeignKey('user.id'), index=True, nullable=False)
    from_user: Mapped["User"] = relationship(
        "User",
        backref="from_orders",
        foreign_keys=[from_user_id])

    to_user_id = Column(ForeignKey('user.id'), index=True, nullable=False)
    to_user: Mapped["User"] = relationship(
        "User",
        backref="to_orders",
        foreign_keys=[to_user_id])

    from_currency = Column(ForeignKey('currency.id'), nullable=False)
    to_currency = Column(ForeignKey('currency.id'), nullable=False)

    status = Column(SmallInteger, nullable=False)

    created_at = Column(DateTime(timezone=True), index=True, default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
