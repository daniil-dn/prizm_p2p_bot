from aiogram import Router

from . import new_order, dialog

router = Router()
router.include_routers(
    new_order.router,
    dialog.new_order_dialog
)
