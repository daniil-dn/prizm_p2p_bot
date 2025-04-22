from logging import getLogger

import aiohttp

from app.core.config import settings
from app.core.dao import crud_prizm_node_ip

logger = getLogger(__name__)


class PrizmWalletFetcher:
    def __init__(self, ip=None):
        if ip:
            self.ip = ip
            self.base_url =  settings.PRIZM_API_URL.format(prizm_node_ip=ip)

    async def init_with_active_node(self, session):
        node = await crud_prizm_node_ip.get_active(session)
        if not node:
            self.ip = None
            self.base_url = None
        else:
            self.ip = node.ip
            self.base_url = settings.PRIZM_API_URL.format(prizm_node_ip=node.ip)
        return self

    async def get_balance(self, account):
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}?requestType=getBalance&account={account}"
            async with session.get(url) as response:
                res = await response.json(content_type=None)
        logger.debug(f'Get balance. node {self.ip}: {res}')
        if res.get('errorCode'):
            raise Exception(res)
        return res

    async def check_node(self):
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}"
            async with session.get(url) as response:
                res = await response.json(content_type=None)
        logger.debug(f'Check node {self.ip}: {res}')
        return res

    async def get_blockchain_transactions(self, account):
        url = f"{self.base_url}?account={account}&requestType=getBlockchainTransactions"
        async with aiohttp.ClientSession() as session:
            async with session.post(url) as response:
                res = await response.json(content_type=None)
            await session.close()
        logger.debug(f'Get blockchain txns: {res}')
        if res.get('errorCode'):
            raise Exception(res)
        return res

    async def read_message(self, secret_phrase, transaction):
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}?requestType=readMessage&secretPhrase={secret_phrase}&transaction={transaction}"
            async with session.get(url) as response:
                res = await response.json(content_type=None)
            await session.close()
        if res.get('errorCode'):
            raise Exception(res)
        logger.info(f'Read message for {transaction}: {res}')
        return res

    async def send_money(self, recipient, secret_phrase, amount_nqt, deadline):

        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}?requestType=sendMoney"
            params = {
                'recipient': recipient,
                'secretPhrase': secret_phrase,
                'amountNQT': amount_nqt,
                'deadline': deadline
            }
            async with session.post(url, params=params) as response:
                res = await response.json(content_type=None)
            await session.close()
        logger.info(f'Send money to {recipient} {amount_nqt} PZM: {res}')
        if res.get('errorCode'):
            raise Exception(res)
        return res
