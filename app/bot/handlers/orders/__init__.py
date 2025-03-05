from aiogram import Router

from . import accept_cancel_cb
from .accept_order_payment import accept_order_payment_cb

router = Router()
router.include_routers(
    accept_cancel_cb.router,
    accept_order_payment.router,
)
