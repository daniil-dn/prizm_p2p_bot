from logging import getLogger
from typing import List

from app.core import dto
from app.core.config import settings
from app.core.dao import crud_prizm_node_ip
from app.core.models import PrizmNodeIp
from app.prizm_check_scheduler.prizm_fetcher import PrizmWalletFetcher

logger = getLogger(__name__)

async def prizm_node_ip_check_sheduled(session):
    async with session() as session:
        nodes: List[PrizmNodeIp] = await crud_prizm_node_ip.get_all(session)
        for node in nodes:
            upd_is_active = False
            try:
                await PrizmWalletFetcher(node.ip).check_node()
                await PrizmWalletFetcher(node.ip).get_balance(settings.PRIZM_WALLET_ADDRESS)
                upd_is_active = True
            except Exception as err:
                logger.info(f"Check node error: {err}")
                upd_is_active = False
            await crud_prizm_node_ip.update(db=session, db_obj=node,
                                            obj_in=dto.PrizmNodeIPUpdate(is_active=upd_is_active))