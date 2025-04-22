def get_start_text(balance, referral_balance, order_count, cancel_order_count):
    return f"""Ваш баланс: {balance} PZM
Ваш реферальный баланс: {referral_balance}
Кол-во сделок: {order_count}
Кол-во отказов: {cancel_order_count}"""
