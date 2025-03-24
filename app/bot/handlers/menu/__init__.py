from aiogram import Router

from . import rules, support, profile, transfer_to_myhome, admin, withdraw_money, partner_system

router = Router()
router.include_routers(
    rules.router,
    support.router,
    profile.router,
    transfer_to_myhome.router,
    withdraw_money.router,
    admin.router,
    partner_system.router
)
