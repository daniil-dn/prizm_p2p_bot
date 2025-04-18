from logging import getLogger

import aiohttp

logger = getLogger(__name__)


class PrizmWalletFetcher:
    def __init__(self, base_url):
        self.base_url = base_url

    async def get_balance(self, account):
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}?requestType=getBalance&account={account}"
            async with session.get(url) as response:
                return await response.json(content_type=None)

    async def get_blockchain_transactions(self, account):
        url = f"{self.base_url}?account={account}&requestType=getBlockchainTransactions"
        async with aiohttp.ClientSession() as session:
            async with session.post(url) as response:
                res = await response.json(content_type=None)
            await session.close()
        logger.debug(f'Get blockchain txns: {res}')
        return res

    async def read_message(self, secret_phrase, transaction):
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}?requestType=readMessage&secretPhrase={secret_phrase}&transaction={transaction}"
            async with session.get(url) as response:
                res = await response.json(content_type=None)
            await session.close()

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
