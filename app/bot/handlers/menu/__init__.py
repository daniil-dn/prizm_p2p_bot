from aiogram import Router

from . import rules, support, profile, transfer_to_myhome

router = Router()
router.include_routers(
    rules.router,
    support.router,
    profile.router,
    transfer_to_myhome.router,
)
