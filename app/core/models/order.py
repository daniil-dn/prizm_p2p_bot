from sqlalchemy import Column, BigInteger, func, ForeignKey, Index, SmallInteger, Numeric, String, DateTime

from sqlalchemy.orm import relationship, Mapped

from app.core.db.base_class import Base
from app.core.models.model_base import ModelBase


class Order(Base, ModelBase):
    CREATED = 1
    ACCEPTED = 2
    IN_PROGRESS = 3
    WAIT_DONE_TRANSFER = 4
    DONE = 5
    CANCELED = 6

    __table_args__ = (
        Index('ix_seller_buyer', "from_user_id", "to_user_id"),
    )

    id = Column(BigInteger, primary_key=True)
    from_user_id = Column(ForeignKey('user.id'), index=True, nullable=False)
    from_user: Mapped["User"] = relationship(
        "User",
        back_populates="from_orders",
        foreign_keys=[from_user_id])

    to_user_id = Column(ForeignKey('user.id'), index=True, nullable=False)
    to_user: Mapped["User"] = relationship(
        "User",
        back_populates="to_orders",
        foreign_keys=[to_user_id])

    from_currency = Column(String(5), nullable=False)
    to_currency = Column(String(5), nullable=False)

    order_request_id = Column(ForeignKey('order_request.id'), nullable=False)

    prizm_value = Column(Numeric(18, 4, asdecimal=False), nullable=False)
    rub_value = Column(Numeric(18, 4, asdecimal=False), nullable=False)

    commission_percent = Column(Numeric(18, 2, asdecimal=False), nullable=False)

    status = Column(SmallInteger, nullable=False)
    mode = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), index=True, default=func.now())
    updated_at = Column(DateTime(timezone=True), index=True, onupdate=func.now())
