from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Cancel, Group, Button, ListGroup, Select, Row, SwitchTo, Back, ScrollingGroup
from aiogram_dialog.widgets.text import Const, Format, List, Case

from app.bot.handlers.partner_system.callbacks import back_to_partner, select_chat, error_number, error_interval, \
    continue_chat, stop_chat, update_count, update_interval, update_interval_in_day
from app.bot.handlers.partner_system.filter import interval_in_day_filter
from app.bot.handlers.partner_system.getters import chats_getter, chat_getter
from app.bot.handlers.partner_system.states import UpdateChannel
from app.utils.text_check import check_interval


def get_chats() -> Window:
    return Window(
        Case(
            {
                True: Format('{text}'),
                False: Const('У вас нет чатов')
            },
            selector='there'
        ),
        ScrollingGroup(
            Select(
                Format("✏️ {item[title]}"),
                id="select_chat",
                on_click=select_chat,
                item_id_getter=lambda item: item['id'],
                items="chats",
                when='there'
            ),
            hide_on_single_page=True,
            height=7,
            width=1,
            id="select_chat_scroll",
        ),
        Button(Const("🔙Назад"), id="start_bot", on_click=back_to_partner),
        state=UpdateChannel.select_chat,
        getter=chats_getter
    )


def get_options() -> Window:
    return Window(
        Format('{text}'),
        SwitchTo(text=Const('Кол-во в день'), id='count_in_day', state=UpdateChannel.count_in_day),
        SwitchTo(text=Const('Время между постами'), id='interval', state=UpdateChannel.interval),
        SwitchTo(text=Const('Интервал в течение дня'), id='interval_in_day', state=UpdateChannel.interval_in_day),
        Button(text=Const('▶️продолжить постинг'), id='continue_post', on_click=continue_chat, when=F['chat'].is_stopped),
        Button(text=Const('⏸️Остановить постинг'), id='stop_post', on_click=stop_chat, when=~F['chat'].is_stopped),

        Back(Const("🔙Назад")),
        state=UpdateChannel.select_option,
        getter=chat_getter
    )


def update_count_in_day() -> Window:
    return Window(
        Const('Введите новое значение, количество постов в день'),
        TextInput(id='get_count', on_success=update_count, on_error=error_number, type_factory=int),
        SwitchTo(Const("🔙Назад"), id='back_change_settings', state=UpdateChannel.select_option),
        state=UpdateChannel.count_in_day,
        getter=chat_getter
    )


def update_interval_window() -> Window:
    return Window(
        Const('Введите новое значение, время между постами'),
        TextInput(id='get_interval', on_success=update_interval, on_error=error_number, type_factory=int),
        SwitchTo(Const("Назад"), id='back_change_settings', state=UpdateChannel.select_option),
        state=UpdateChannel.interval,
        getter=chat_getter
    )


def update_interval_in_day_window() -> Window:
    return Window(
        Const('Введите интервал в течение дня (в формате 09:00-21:00)'),
        TextInput(id='get_interval_in_day', on_success=update_interval_in_day, on_error=error_interval, filter=interval_in_day_filter),
        SwitchTo(Const("🔙Назад"), id='back_change_settings', state=UpdateChannel.select_option),
        state=UpdateChannel.interval_in_day,
        getter=chat_getter
    )
