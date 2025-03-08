from sqlalchemy import Column, DateTime, BigInteger, func, ForeignKey, \
    Numeric, String, JSON

from app.core.db.base_class import Base
from app.core.models.model_base import ModelBase


class Transaction(Base, ModelBase):
    id = Column(BigInteger, primary_key=True)
    transaction_id = Column(String, index=True, nullable=False)
    from_wallet_address = Column(String, index=True, nullable=False)
    to_wallet_address = Column(String, index=True, nullable=False)

    value = Column(Numeric(18, 4, asdecimal=False), nullable=False)
    fee = Column(Numeric(18, 4, asdecimal=False), nullable=False)

    order_id = Column(ForeignKey('order.id'), index=True, nullable=True)
    order_request_id = Column(ForeignKey('order_request.id'), index=True, nullable=True)
    user_id = Column(ForeignKey('user.id'), index=True, nullable=True)

    message_text = Column(String, nullable=True)

    type = Column(String, nullable=True)

    extra_data = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), index=True, default=func.now())
