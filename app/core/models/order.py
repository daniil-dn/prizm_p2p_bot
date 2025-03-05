from sqlalchemy import Column, DateTime, BigInteger, func, ForeignKey, Index, SmallInteger, Numeric, String

from sqlalchemy.orm import relationship, Mapped

from app.core.db.base_class import Base
from app.core.models.model_base import ModelBase
from app.core.models.user import User


class Order(Base, ModelBase):
    CREATED = 1
    ACCEPTED = 2
    IN_PROGRESS = 3
    WAIT_DONE_TRANSFER = 4
    DONE = 4
    CANCELED = 4

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

    order_request_id = Column(ForeignKey('order_request.id'), nullable=False)

    from_value = Column(Numeric(18, 4, asdecimal=False), nullable=False)
    to_value = Column(Numeric(18, 4, asdecimal=False), nullable=False)

    commission_percent = Column(Numeric(18, 2, asdecimal=False), nullable=False)

    status = Column(SmallInteger, nullable=False)
    mode = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), index=True, default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
