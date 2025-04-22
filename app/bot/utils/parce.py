from datetime import timedelta, datetime

from pytz import timezone
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dao import crud_user, crud_settings, crud_order
from app.core.db import session


def parce_time(last_online: datetime):
    if not last_online:
        time_text = f'🔓Был(а) давно (мск)'
    elif datetime.now(tz=timezone('utc')) - last_online < timedelta(minutes=15):
        last_online = (last_online + timedelta(hours=3)).strftime("%H:%M")
        time_text = f'✅Был(а) в {last_online} (мск)'
    elif datetime.now(tz=timezone('utc')).date() == last_online.date():
        last_online = (last_online + timedelta(hours=3)).strftime("%H:%M")
        time_text = f'🔓Был(а) в {last_online} (мск)'
    else:
        last_online = (last_online + timedelta(hours=3)).strftime("%H:%M %d.%m.%Y")
        time_text = f'🔓Был(а) в {last_online} (мск)'
    return time_text

def get_invites_by_level(grouped_descendants: dict):
    sorted_levels = sorted(grouped_descendants.keys())
    result = []
    for level in sorted_levels:
        result.extend([grouped_descendants[level]])
    return result

async def get_partner_data(session: AsyncSession, user_id: int):
    user_db = await crud_user.get_by_id(session, id=user_id)
    users_invites  = await crud_user.get_descendant_users(session, user_db=user_db)
    grouped_descendants = get_invites_by_level(users_invites)
    settings = await crud_settings.get_by_id(session, id=1)


    result = {}
    partner_commissions = [0.06, 0.03, 0.01]
    for level in range(3):
        count_orders = 0
        summ = 0
        bot_commission_summ = 0
        partner_level_commission_summ = 0
        level_users = grouped_descendants[level] if len(grouped_descendants) >= level+1 else []
        for user in level_users:
            orders = await crud_order.get_sell_orders(session, user_id=user.id)
            count_orders += user.order_count
            summ += sum(order.prizm_value for order in orders)
            bot_commission_summ += sum(order.prizm_value*order.commission_percent for order in orders)
            partner_level_commission_summ += sum(order.prizm_value*order.commission_percent*partner_commissions[level] for order in orders)

        result[level] = {
            'summ': summ,
            'bot_commission_summ': bot_commission_summ,
            'partner_level_commission_summ': partner_level_commission_summ,
            'count_orders': count_orders,
            'user_count': len(level_users),
        }
    return {
        "descendants_result": result,
        'percent': settings.partner_commission_percent
    }