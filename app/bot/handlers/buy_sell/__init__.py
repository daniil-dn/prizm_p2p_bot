from aiogram import Router

from . import buy_sell_mode, dialog

router = Router()
router.include_routers(
    buy_sell_mode.router,
    dialog.buy_sell_dialog
)
