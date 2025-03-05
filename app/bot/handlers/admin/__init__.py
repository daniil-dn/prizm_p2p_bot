from aiogram import Router

from . import common, bot_settings

router = Router()
router.include_routers(
    common.router,
    bot_settings.router,
)
