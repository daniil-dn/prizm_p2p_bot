from aiogram import Router

from . import rules, support, profile, transfer_to_myhome, admin, my_order_requests

router = Router()
router.include_routers(
    rules.router,
    support.router,
    profile.router,
    transfer_to_myhome.router,
    my_order_requests.router,
    admin.router
)
