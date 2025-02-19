def get_routers() -> tuple:
    from . import (
        common,
        menu,
        buy_sell
    )

    return (
        common.router,
        menu.router,
        buy_sell.router
    )
