from typing import Any
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.input import TextInput
from aiogram.types import Message
from aiogram_dialog import (
    DialogManager,
    Window
)

from app.bot.handlers.admin.bot_settings.handlers import cancel_logic, on_new_wait_order_time, \
    on_new_commission_percent_value, on_pay_order_time_value, on_prizm_rate_diff_value, on_add_admin_username_value, \
    on_remove_admin_username_value, on_new_withdrawal_commission_percent_value
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
        Const("Изменение времени ожидания нового ордера\nНовое значение в минутах"),

        TextInput(id="new_value", on_success=on_new_wait_order_time, on_error=error,
                  type_factory=float),
        Button(Const("❌ Отмена"), id="cancel", on_click=cancel_logic),
        state=AdminSettingsState.new_order_time,
    )


def get_new_commission_value() -> Window:
    return Window(
        Const("Изменение комиссии \nНовое значение в процентах. Например 10"),
        TextInput(id="new_value", on_success=on_new_commission_percent_value, on_error=error,
                  type_factory=int),
        Button(Const("❌ Отмена"), id="cancel", on_click=cancel_logic),
        state=AdminSettingsState.new_value_commission,
    )

def get_new_withdrawal_commission_value() -> Window:
    return Window(
        Const("Изменение комиссии вывода \nНовое значение в процентах. Например 10"),
        TextInput(id="new_value", on_success=on_new_withdrawal_commission_percent_value, on_error=error,
                  type_factory=int),
        Button(Const("❌ Отмена"), id="cancel", on_click=cancel_logic),
        state=AdminSettingsState.new_value_withdrawal_commission,
    )



def get_pay_order_time_value() -> Window:
    return Window(
        Const("Изменение времени ожидания оплаты ордера\nНовое значение в минутах. Например 20"),
        TextInput(id="new_value", on_success=on_pay_order_time_value, on_error=error,
                  type_factory=float),
        Button(Const("❌ Отмена"), id="cancel", on_click=cancel_logic),
        state=AdminSettingsState.new_pay_order_time,
    )


def get_prizm_rate_diff_value() -> Window:
    return Window(
        Const("Изменение процента разницы курса\n Новое значение в процентах. Например 20"),
        TextInput(id="new_value", on_success=on_prizm_rate_diff_value, on_error=error,
                  type_factory=int),
        Button(Const("❌ Отмена"), id="cancel", on_click=cancel_logic),
        state=AdminSettingsState.new_prizm_rate_diff_value,
    )


def add_admin_by_username() -> Window:
    return Window(
        Const("Введите username нового админа. Например test_username"),
        TextInput(id="new_value", on_success=on_add_admin_username_value, on_error=error,
                  type_factory=str),
        Button(Const("❌ Отмена"), id="cancel", on_click=cancel_logic),
        state=AdminSettingsState.add_admin_by_username,
    )


def remove_admin_by_username() -> Window:
    return Window(
        Const("Введите username нового админа. Например test_username"),
        TextInput(id="new_value", on_success=on_remove_admin_username_value, on_error=error,
                  type_factory=str),
        Button(Const("❌ Отмена"), id="cancel", on_click=cancel_logic),
        state=AdminSettingsState.remove_admin_by_username,
    )
