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

from app.bot.handlers.admin.bot_settings.handlers import cancel_logic, on_new_wait_order_time, \
    on_new_commission_percent_value, on_pay_order_time_value
from app.bot.handlers.admin.state import AdminSettingsState


async def error(
        message: Message,
        dialog_: Any,
        manager: DialogManager,
        error_: ValueError
):
    await message.answer("Введите корректную сумму")


def get_new_wait_order_time() -> Window:
    return Window(
        Const("Новое значение в минутах"),

        TextInput(id="new_value", on_success=on_new_wait_order_time, on_error=error,
                  type_factory=float),
        Button(Const("❌ Отмена"), id="cancel", on_click=cancel_logic),
        state=AdminSettingsState.new_order_time,
    )


def get_new_commission_value() -> Window:
    return Window(
        Const("Новое значение в процентах. Например 20"),
        TextInput(id="new_value", on_success=on_new_commission_percent_value, on_error=error,
                  type_factory=float),
        Button(Const("❌ Отмена"), id="cancel", on_click=cancel_logic),
        state=AdminSettingsState.new_value_commission,
    )


def get_pay_order_time_value() -> Window:
    return Window(
        Const("Новое значение в минутах. Например 20"),
        TextInput(id="new_value", on_success=on_pay_order_time_value, on_error=error,
                  type_factory=float),
        Button(Const("❌ Отмена"), id="cancel", on_click=cancel_logic),
        state=AdminSettingsState.new_pay_order_time,
    )
