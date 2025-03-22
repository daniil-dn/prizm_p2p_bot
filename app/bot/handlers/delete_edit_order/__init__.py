from aiogram import Router

from . import start_dialog, dialog

router = Router()
router.include_routers(
    start_dialog.router,
    dialog.router
)
