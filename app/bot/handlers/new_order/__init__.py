from aiogram import Router

from . import new_order, dialog, common

router = Router()
router.include_routers(
    new_order.router,
    dialog.new_order_dialog,
    common.router
)
