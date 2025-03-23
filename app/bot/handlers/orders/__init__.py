from aiogram import Router

from . import accept_cancel_cb
from . import accept_order_payment
from . import communications
from . import back

router = Router()
router.include_routers(
    accept_cancel_cb.router,
    accept_order_payment.router,
    communications.router,
    back.router
)
