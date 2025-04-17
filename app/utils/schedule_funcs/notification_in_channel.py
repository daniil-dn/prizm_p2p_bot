from datetime import datetime, timedelta

from pytz import timezone
from aiogram import Bot

from app.bot.ui.partner_system import url_button
from app.bot.utils.parce import parce_time
from app.core.config import settings
from app.core.dao import crud_chat_channel, crud_order_request
from app.utils.coinmarketcap import get_currency_rate


async def notification_sheduled(bot: Bot, session):
    async with session() as session:
        chats = await crud_chat_channel.get_all_active(session)
        best_order_to_buy = await crud_order_request.get_best_buy(session)
        best_order_to_sell = await crud_order_request.get_best_sell(session)

    buy_last_online_text = parce_time(best_order_to_buy.user.last_online)
    sell_last_online_text = parce_time(best_order_to_sell.user.last_online)
    rate = await get_currency_rate("PZM", "RUB", settings.COINMARKETCAP_API_KEY)
    now = datetime.now(tz=timezone('Europe/Moscow'))

    text = ('Prizm Exchange\n\n'
            f'Курс руб/PZM {now.strftime("%H:%M")} на {now.strftime("%d.%m.%y")} - {rate:.4f}\n\n'
            'Самый выгодный ордер на покупку:\n\n'
            f'Ордер : №{best_order_to_buy.id}\n'
            f'Курс 1pzm - {best_order_to_buy.rate:.3f} руб\n'
            f'Лимит: {best_order_to_buy.min_limit} - {best_order_to_buy.max_limit} PZM\n'
            f'Число сделок: {best_order_to_buy.user.order_count}\n'
            f'Число отказов: {best_order_to_buy.user.cancel_order_count}\n'
            f'{buy_last_online_text}\n\n'
            f'Самый выгодный ордер на продажу:\n\n'
            f'Ордер: №{best_order_to_sell.id}\n'
            f'Курс 1pzm - {best_order_to_sell.rate:.3f} руб\n'
            f'Лимит: {best_order_to_sell.min_limit_rub} - {best_order_to_sell.max_limit_rub} руб\n'
            f'Число сделок: {best_order_to_sell.user.order_count}\n'
            f'Число отказов: {best_order_to_sell.user.cancel_order_count}\n'
            f'{sell_last_online_text}\n\n')

    chats = [chat for chat in chats if
             chat.current_count < chat.count_in_day and
             now >= (chat.last_post or datetime.fromtimestamp(0, timezone('Europe/Moscow'))) + timedelta(minutes=chat.interval)]

    for chat in chats:
        start_time_str, end_time_str = chat.interval_in_day.split("-")

        start_time = datetime.strptime(start_time_str, "%H:%M").time()
        end_time = datetime.strptime(end_time_str, "%H:%M").time()

        if not (start_time <= now.time() <= end_time):
            continue

        link = f'https://t.me/{(await bot.get_me()).username}' + '?start=' + hex(chat.user_id)

        try:
            await bot.send_message(chat.id, text, reply_markup=url_button(link))
            await crud_chat_channel.update(session, obj_in={'id': chat.id,
                                                            'current_count': chat.current_count + 1,
                                                            'last_post': now})
        except Exception as e:
            print(e)

