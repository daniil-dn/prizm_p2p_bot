from aiogram_dialog import ShowMode
from typing import Any
from aiogram_dialog.widgets.kbd import Button, Back
from aiogram_dialog.widgets.text import Const, Format, Case
from aiogram_dialog.widgets.input import TextInput
from aiogram.types import Message
from aiogram_dialog import (
    DialogManager,
    Window
)

from app.bot.handlers.new_order.getters import get_mode, get_prizm_rate
from app.bot.handlers.new_order.handlers import on_back, on_from_value_selected, on_to_value_selected, cancel_logic, \
    on_rate_selected, on_sell_card_info_selected, on_card_method_selected
from app.bot.handlers.new_order.state import NewOrderState


async def error(
        message: Message,
        dialog_: Any,
        manager: DialogManager,
        error_: ValueError
):
    await message.answer("Введите корректную сумму.")


async def error_rate(
        message: Message,
        dialog_: Any,
        manager: DialogManager,
        error_: ValueError
):
    await message.answer("Введите курс с точкой")


def get_from_value() -> Window:
    return Window(
        Case(
            {
                'buy': Const("Укажите в Prizm минимальную сумму покупки"),
                'sell': Const("Укажите в Prizm минимальную сумму продажи"),
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
                'buy': Const("Укажите в Prizm максимальную сумму покупки"),
                'sell': Const("Укажите в Prizm максимальную сумму продажи"),
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
            "Укажите желаемую стоимость PRIZM в рублях.\nТекущий курс <b>{prizm_rate}</b> PZM/RUB https://coinmarketcap.com/currencies/prizm .\nРазница указанного вами курса не должна отличаться более чем на <b>{prizm_rate_diff_percent}</b>%"),

        TextInput(id="rate", on_success=on_rate_selected, on_error=error_rate,
                  type_factory=float),
        Button(Const("❌ Отмена"), id="cancel", on_click=cancel_logic),
        Button(Const("❌ Назад"), id="back", on_click=Back(show_mode=ShowMode.DELETE_AND_SEND)),
        getter=get_prizm_rate,
        state=NewOrderState.rate,
        parse_mode='html'
    )


def get_wallet_method() -> Window:
    return Window(
        Const("Укажите способ получения оплаты"),
        Button(text=Const("СБП"), id="sbp", on_click=on_card_method_selected),
        Button(text=Const("Карта"), id="card", on_click=on_card_method_selected),
        Button(Const("❌ Отмена"), id="cancel", on_click=cancel_logic),
        Button(Const("❌ Назад"), id="back", on_click=Back(show_mode=ShowMode.DELETE_AND_SEND)),

        state=NewOrderState.card_method_details,
        getter=get_mode
    )


def get_sell_card_info() -> Window:
    return Window(
        Case(
            {
                'buy': Const("Укажите адрес кошелька PRIZM\nПример адреса кошелька: <b> PRIZM-****-****-****-****</b>"),
                'sell': Const("Укажите номер карты (только цифры)"),
                'sbp': Const("Укажите номер телефона (только цифры) и банк\nПример: +79181081081 Сбербанк"),
            },
            selector='mode',
        ),

        TextInput(id="sell_card_info", on_success=on_sell_card_info_selected, on_error=error,
                  type_factory=str),
        Button(Const("❌ Отмена"), id="cancel", on_click=cancel_logic),
        Button(Const("❌ Назад"), id="back", on_click=on_back),
        getter=get_mode,
        state=NewOrderState.sell_card_info,
        parse_mode='html'
    )
