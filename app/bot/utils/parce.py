from datetime import timedelta, datetime

from pytz import timezone


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