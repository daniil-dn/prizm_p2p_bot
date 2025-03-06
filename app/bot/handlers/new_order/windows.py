from datetime import date, timedelta, timezone

from aiogram import F
from aiogram_dialog import Window, ShowMode
from typing import Any
from aiogram_dialog.widgets.kbd import Button, Group, ScrollingGroup, Select, Calendar, CalendarConfig, Back, Cancel, \
    Next, StubScroll, LastPage, NextPage, CurrentPage, PrevPage, FirstPage, Row, Column, NumberedPager
from aiogram_dialog.widgets.text import Const, Format, Case
from aiogram_dialog.widgets.input import TextInput
from aiogram.types import Message
from aiogram_dialog import (
    Dialog,
    DialogManager,
    Window
)

from app.bot.handlers.new_order.getters import get_mode, get_prizm_rate
from app.bot.handlers.new_order.handlers import on_back, on_from_value_selected, on_to_value_selected, cancel_logic, \
    on_rate_selected, on_sell_card_info_selected
from app.bot.handlers.new_order.state import NewOrderState


async def error(
        message: Message,
        dialog_: Any,
        manager: DialogManager,
        error_: ValueError
):
    await message.answer("Введите корректную сумму")


def get_from_value() -> Window:
    return Window(
        Case(
            {
                'buy': Const("Укажите от какой суммы покупка PRIZM"),
                'sell': Const("Укажите от какой суммы продажа PRIZM"),
            },
            selector='mode',
        ),
        TextInput(id="from_value", on_success=on_from_value_selected, on_error=error,
                  type_factory=float),
        Button(Const("❌ Отмена"), id="cancel", on_click=cancel_logic),
        state=NewOrderState.from_value,
        getter=get_mode
    )


def get_to_value() -> Window:
    return Window(
        Case(
            {
                'buy': Const("Укажите до какой суммы покупка в PRIZM"),
                'sell': Const("Укажите до какой суммы продажа в PRIZM"),
            },
            selector='mode',
        ),
        TextInput(id="to_value", on_success=on_to_value_selected, on_error=error,
                  type_factory=float),
        Button(Const("❌ Отмена"), id="cancel", on_click=cancel_logic),
        Button(Const("❌ Назад"), id="back", on_click=Back(show_mode=ShowMode.DELETE_AND_SEND)),

        state=NewOrderState.to_value,
        getter=get_mode
    )


def get_rate() -> Window:
    return Window(
        Format(
            "Укажите желаемую стоимость PRIZM.\nТекущий курс <b>{prizm_rate}</b>.\nРазница указанного курса не должна отличаться более чем на <b>{prizm_rate_diff_percent}</b>%"),

        TextInput(id="rate", on_success=on_rate_selected, on_error=error,
                  type_factory=float),
        Button(Const("❌ Отмена"), id="cancel", on_click=cancel_logic),
        Button(Const("❌ Назад"), id="back", on_click=Back(show_mode=ShowMode.DELETE_AND_SEND)),
        getter=get_prizm_rate,
        state=NewOrderState.rate,
        parse_mode='html'
    )


def get_sell_card_info() -> Window:
    return Window(
        Case(
            {
                'buy': Const("Укажите адрес кошелька PRIZM\nПример адреса кошелька: <b> PRIZM-****-****-****-****</b>"),
                'sell': Const("Укажите реквизиты для получения рублей"),
            },
            selector='mode',
        ),

        TextInput(id="sell_card_info", on_success=on_sell_card_info_selected, on_error=error,
                  type_factory=str),
        Button(Const("❌ Отмена"), id="cancel", on_click=cancel_logic),
        Button(Const("❌ Назад"), id="back", on_click=Back(show_mode=ShowMode.DELETE_AND_SEND)),
        getter=get_mode,
        state=NewOrderState.sell_card_info,
        parse_mode='html'
    )
