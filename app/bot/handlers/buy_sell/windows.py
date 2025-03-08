from aiogram_dialog import ShowMode
from typing import Any
from aiogram_dialog.widgets.kbd import Group, Select, Back, \
    StubScroll, LastPage, NextPage, PrevPage, FirstPage, Row, Column, NumberedPager
from aiogram_dialog.widgets.text import Const, Format, Case
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button
from aiogram.types import Message
from aiogram_dialog import (
    DialogManager,
    Window
)

from app.bot.handlers.buy_sell.getters import get_orders_getter, get_mode, get_order_accept_wait_time
from app.bot.handlers.buy_sell.handlers import cancel_logic, \
    process_order_request_selected, \
    on_card_info_input, on_back, on_accept_order_request_input, on_value_selected
from app.bot.handlers.buy_sell.state import BuyState


async def error(
        message: Message,
        dialog_: Any,
        manager: DialogManager,
        error_: ValueError
):
    await message.answer("Введите корректную сумму")


def get_value() -> Window:
    return Window(
        Case(
            {
                'buy': Const("Укажите на какую сумму покупку в RUB"),
                'sell': Const("Укажите на какую сумму продажа в PRIZM"),
            },
            selector='mode'
        ),
        TextInput(id="from_value", on_success=on_value_selected, on_error=error,
                  type_factory=float),
        Button(Const("❌ Отмена"), id="cancel", on_click=cancel_logic),
        state=BuyState.exact_value,
        getter=get_mode
    )


def get_wallet_info() -> Window:
    return Window(
        Case(
            {
                'buy': Const("Укажите адрес кошелька prizm\nПример адреса кошелька: PRIZM-****-****-****-****"),
                'sell': Const("Укажите реквизиты карты"),
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
        Format("Поиск ордеров по вашему запросу:\n{all_orders_text}"),
        Group(
            Column(
                Select(
                    Format("✅{item[order_text]}"),
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
        Format("Подтвердите ордер. У вас есть {wait_time} минут на подтверждение"),
        Button(text=Const("✅Подтвердить"), id="accept_order", on_click=on_accept_order_request_input),
        Button(Const("❌ Отмена"), id="cancel", on_click=cancel_logic),
        Button(Const("❌ Назад"), id="back", on_click=Back(show_mode=ShowMode.DELETE_AND_SEND)),

        state=BuyState.accept_order_request,
        getter=get_order_accept_wait_time
    )
