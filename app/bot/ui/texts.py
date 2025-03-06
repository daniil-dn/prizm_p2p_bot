def get_start_text(balance, order_count, cancel_order_count):
    return f"""Ваш баланс: {balance}
Кол-во сделок: {order_count}
Кол-во отказов: {cancel_order_count}"""
