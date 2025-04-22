def get_routers() -> tuple:
    from . import (
        common,
        menu,
        buy_sell,
        new_order,
        orders,
        admin,
        delete_edit_order,
        partner_system
    )

    return (
        common.router,
        menu.router,
        orders.router,
        admin.router,
        buy_sell.router,
        new_order.router,
        delete_edit_order.router,
        partner_system.router,
    )
