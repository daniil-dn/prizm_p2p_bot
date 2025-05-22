from logging import getLogger

import aiohttp

logger = getLogger(__name__)


async def get_currency_rate(from_currency, to_currency, api_key):
    # URL для запроса данных о курсе Prizm
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

    # Параметры запроса
    params = {
        'symbol': from_currency,
        'convert': to_currency
    }

    # Заголовки запроса
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as response:
            data = await response.json()

    # Получение курса Prizm к рублю
    if 'data' in data and from_currency in data['data']:
        price = data['data'][from_currency]['quote'][to_currency]['price']
        logger.info(f'Курс {from_currency} к {to_currency}: {price} RUB')
        return price
    else:
        logger.info(f'Данные о курсе {from_currency} не найдены error:{data}')


def rate_difference(rate, value, diff):
    difference = abs(rate - value)
    average = (abs(rate) + abs(value)) / 2
    percentage_difference = (difference / average) * 100
    if percentage_difference <= diff:
        return False
    else:
        return True
