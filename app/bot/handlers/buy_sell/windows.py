from datetime import date, timedelta, timezone
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

from app.bot.handlers.buy_sell.getters import get_orders_getter, get_mode
from app.bot.handlers.buy_sell.handlers import on_to_value_selected, on_from_value_selected, cancel_logic, \
    process_order_request_selected, \
    on_card_info_input, on_back, on_exactly_value_input
from app.bot.handlers.buy_sell.state import BuyState


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
                'buy': Const("Укажите от какой суммы покупка в рублях"),
                'sell': Const("Укажите от какой суммы продажа в рублях"),
            },
            selector='mode'
        ),
        TextInput(id="from_value", on_success=on_from_value_selected, on_error=error,
                  type_factory=float),
        Button(Const("❌ Отмена"), id="cancel", on_click=cancel_logic),
        state=BuyState.from_value,
        getter=get_mode
    )


def get_to_value() -> Window:
    return Window(
        Case(
            {
                'buy': Const("Укажите до какой суммы покупка в рублях"),
                'sell': Const("Укажите до какой суммы продажа в рублях"),
            },
            selector='mode',
        ),
        TextInput(id="to_value", on_success=on_to_value_selected, on_error=error,
                  type_factory=float),
        Button(Const("❌ Отмена"), id="cancel", on_click=cancel_logic),
        state=BuyState.to_value,
        getter=get_mode
    )


def get_wallet_info() -> Window:
    return Window(
        Case(
            {
                'buy': Const("Укажите адрес кошелька prizm"),
                'sell': Const("Укажите реквезиты карты"),
            },
            selector='mode',
        ),
        TextInput(id="card_info", on_success=on_card_info_input, on_error=error,
                  type_factory=str),
        Button(Const("❌ Отмена"), id="cancel", on_click=cancel_logic),
        Button(Const("❌ Назад"), id="back", on_click=Back(show_mode=ShowMode.DELETE_AND_SEND)),

        state=BuyState.card_details,
        getter=get_mode
    )


def orders_list() -> Window:
    """Окно выбора количества гостей."""
    return Window(
        Const("Поиск ордеров по вашему запросу:"),
        Group(
            Column(
                Select(
                    Format("{item[order_text]}"),
                    id="order_select",
                    item_id_getter=lambda item: str(item["id"]),
                    items="orders",
                    on_click=process_order_request_selected,

                ),
            ),
            StubScroll(id="ID_STUB_SCROLL", pages="pages"),
            Row(
                FirstPage(
                    scroll="ID_STUB_SCROLL",
                    text=Format("⏮️"),
                ),
                PrevPage(
                    scroll="ID_STUB_SCROLL",
                    text=Format("◀️"),
                ),

                NextPage(
                    scroll="ID_STUB_SCROLL",
                    text=Format("▶️"),
                ),
                LastPage(
                    scroll="ID_STUB_SCROLL",
                    text=Format("⏭️"),
                ),
            ),
        ),
        Button(Const("❌ Отмена"), id="cancel", on_click=cancel_logic),
        Button(Const("❌ Назад"), id="back", on_click=on_back),
        getter=get_orders_getter,
        state=BuyState.orders_list,

    )


def get_exactly_value() -> Window:
    return Window(
        Const("Введите точную сумму в рублях:"),
        TextInput(id="value", on_success=on_exactly_value_input, on_error=error,
                  type_factory=float),
        Button(Const("❌ Отмена"), id="cancel", on_click=cancel_logic),
        Button(Const("❌ Назад"), id="back", on_click=Back(show_mode=ShowMode.DELETE_AND_SEND)),

        state=BuyState.order_exact_value,
    )
