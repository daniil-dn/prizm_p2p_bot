import re


def check_phone_format(text):
    # Регулярное выражение для проверки номера телефона и пробела после
    pattern = r'^\+7\d{10}\s'

    # Выполняем проверку
    return bool(re.match(pattern, text))


def check_card_format(text):
    # Регулярное выражение для проверки номера карты
    pattern = r'^\d{16}'

    # Выполняем проверку
    return bool(re.match(pattern, text))


def check_wallet_format(text):
    # Регулярное выражение для проверки формата кошелька
    pattern = r'^[A-Z]{5}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{5}$'

    # Выполняем проверку
    return bool(re.match(pattern, text))


def check_interval(text):
    pattern = r'(2[0-4])|([01][0-9]):([0-5][0-9])-(2[0-4])|([01][0-9]):([0-5][0-9])'

    return bool(re.match(pattern, text))
