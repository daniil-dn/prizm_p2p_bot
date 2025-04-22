from aiogram import Router

from . import add_chat_channel, withdraw, common, dialog

router = Router()
router.include_routers(
    common.router,
    add_chat_channel.router,
    withdraw.router,
    dialog.router,
)
