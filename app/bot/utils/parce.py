from datetime import timedelta, datetime

from pytz import timezone
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dao import crud_user, crud_settings
from app.core.db import session


def parce_time(last_online: datetime):
    if datetime.now(tz=timezone('utc')) - last_online < timedelta(minutes=15):
        last_online = (last_online + timedelta(hours=3)).strftime("%H:%M")
        time_text = f'✅Был(а) в {last_online} (мск)'
    elif datetime.now(tz=timezone('utc')).date() == last_online.date():
        last_online = (last_online + timedelta(hours=3)).strftime("%H:%M")
        time_text = f'🔓Был(а) в {last_online} (мск)'
    else:
        last_online = (last_online + timedelta(hours=3)).strftime("%H:%M %d.%m.%Y")
        time_text = f'🔓Был(а) в {last_online} (мск)'
    return time_text

async def get_partner_data(session: AsyncSession, user_id: int):
    user_invites = await crud_user.get_invites(session, id=user_id)
    settings = await crud_settings.get_by_id(session, id=1)
    count_orders = 0
    summ = 0
    for user in user_invites:
        count_orders += len(user.to_orders)
        summ += sum(order.prizm_value for order in user.to_orders)

    commission = round(summ * settings.partner_commission_percent, 5)
    return {
        'summ': summ,
        'count_orders': count_orders,
        'count_users': len(user_invites),
        'commission': commission,
        'percent': settings.partner_commission_percent
    }