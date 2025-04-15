from aiogram import Router

from . import add_chat_channel, withdraw, common, update_chat_channels

router = Router()
router.include_routers(
    common.router,
    add_chat_channel.router,
    withdraw.router,
    update_chat_channels.router,
)
