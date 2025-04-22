from aiogram import Router

from . import rules, support, profile, transfer_to_myhome, admin, withdraw_money, create_wallet_prizm

router = Router()
router.include_routers(
    rules.router,
    support.router,
    profile.router,
    transfer_to_myhome.router,
    withdraw_money.router,
    admin.router,
    create_wallet_prizm.router
)
