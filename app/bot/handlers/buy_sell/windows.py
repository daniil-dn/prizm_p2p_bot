from datetime import date, timedelta, timezone
from aiogram_dialog import Window
from typing import Any
from aiogram_dialog.widgets.kbd import Button, Group, ScrollingGroup, Select, Calendar, CalendarConfig, Back, Cancel, \
    Next, StubScroll, LastPage, NextPage, CurrentPage, PrevPage, FirstPage, Row
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput
from aiogram.types import Message
from aiogram_dialog import (
    Dialog,
    DialogManager,
    Window
)

from app.bot.handlers.buy_sell.getters import get_orders_getter
from app.bot.handlers.buy_sell.handlers import on_value_selected, cancel_logic, process_order_request_selected, \
    on_orders_page_changed
from app.bot.handlers.buy_sell.state import BuyState


async def error(
        message: Message,
        dialog_: Any,
        manager: DialogManager,
        error_: ValueError
):
    await message.answer("Введите корректную сумму")


def get_value() -> Window:
    """Окно выбора количества гостей."""
    return Window(
        Const("Укажите сумму покупки в рублях"),
        TextInput(id="value", on_success=on_value_selected, on_error=error,
                  type_factory=float),
        state=BuyState.value
    )


def get_wallet_info() -> Window:
    """Окно выбора количества гостей."""
    return Window(
        Const("Введите реквизиты карты"),
        TextInput(id="value", on_success=Next(), on_error=error,
                  type_factory=float),
        state=BuyState.card_details,
    )


def orders_list_() -> Window:
    """Окно выбора количества гостей."""
    return Window(
        Const("Поиск ордеров по вашему запросу:"),
        Group(
            Row(StubScroll(id="ID_STUB_SCROLL", pages="pages")),
            Row(
                FirstPage(
                    scroll="ID_STUB_SCROLL",
                    text=Format("⏮️ {target_page}"),
                ),
                PrevPage(
                    scroll="ID_STUB_SCROLL",
                    text=Format("◀️"),
                ),
                CurrentPage(
                    scroll="ID_STUB_SCROLL",
                    text=Format("{current_page}"),
                ),
                NextPage(
                    scroll="ID_STUB_SCROLL",
                    text=Format("▶️"),
                ),
                LastPage(
                    scroll="ID_STUB_SCROLL",
                    text=Format("{target_page} ⏭️"),
                ),
            ),
        ),
        getter=get_orders_getter,
        state=BuyState.orders_list,
    )
def orders_list() -> Window:
    """Окно выбора количества гостей."""
    return Window(
        Const("Поиск ордеров по вашему запросу:"),
        ScrollingGroup(
            Select(
                Format("{item[slot_text]}"),
                id="slot_select",
                item_id_getter=lambda item: str(item["id"]),
                items="slots",
                on_click=process_order_request_selected,

            ),
            id="slotes_scrolling",
            width=1,
            height=10,
            on_page_changed=on_orders_page_changed

        ),
        Back(Const("Назад")),
        Cancel(Const("Отмена"), on_click=cancel_logic),
        getter=get_orders_getter,
        state=BuyState.orders_list,
    )
