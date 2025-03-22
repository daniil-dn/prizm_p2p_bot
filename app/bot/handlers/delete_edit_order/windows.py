from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Cancel, Group, Button, ListGroup, Select, Row, SwitchTo
from aiogram_dialog.widgets.text import Const, Format, List, Case

from app.bot.handlers.delete_edit_order.getters import orders_getter, order_getter, get_prizm_rate
from app.bot.handlers.delete_edit_order.handlers import start, order_menu, continue_order, stop_order, delete_order, \
    error_handler, update_min_sum, update_max_sum, update_cource
from app.bot.handlers.delete_edit_order.state import DeleteEditOrder


def get_orders() -> Window:
    return Window(
        Case(
            {
                True: List(
                    Format('{item}'),
                    items='texts',
                    sep='\n\n',
                    id='list_orders_text'
                ),
                False: Const('У вас нет объявлений')
            },
            selector='there'
        ),
        Group(
            Select(
                Format("№{item.id}"),
                id="orders",
                item_id_getter=lambda x: x.id,
                items="orders",
                on_click=order_menu,
            ),
            width=2,
            when='there'
        ),
        Button(Const("❌ Отмена"), id="start_bot", on_click=start),
        state=DeleteEditOrder.orders,
        getter=orders_getter
    )

def get_order_menu() -> Window:
    return Window(
        Format('{text}'),
        Group(
            SwitchTo(
                text=Const('Редактировать'),
                id='update_order',
                state=DeleteEditOrder.update_menu
            ),
            Button(
                text=Const('Остановить'),
                id='stop_order',
                on_click=stop_order,
                when='active'
            ),
            Button(
                text=Const('Возобновить'),
                id='continue_order',
                on_click=continue_order,
                when='stopped'
            ),
            SwitchTo(
                text=Const('Удалить'),
                id='delete_order',
                state=DeleteEditOrder.delete_order
            ),
            width=2,
            id='order_events_row'
        ),
        Button(Const("❌ Отмена"), id="start_bot", on_click=start),
        getter=order_getter,
        state=DeleteEditOrder.order_menu
    )


def delete_order_window() -> Window:
    return Window(
        Const('Введите кошелек для вывода prizm'),
        TextInput(
            id='get_prizm_address',
            on_success=delete_order
        ),
        Button(Const("❌ Отмена"), id="start_bot", on_click=start),
        state=DeleteEditOrder.delete_order
    )


def update_menu_order() -> Window:
    return Window(
        Format('{text}'),
        Group(
            SwitchTo(
                text=Const('Максимальная сумма'),
                id='update_max_sum',
                state=DeleteEditOrder.update_max_sum
            ),
            SwitchTo(
                text=Const('Минимальная сумма'),
                id='update_min_sum',
                state=DeleteEditOrder.update_min_sum
            ),
            SwitchTo(
                text=Const('Курс'),
                id='update_course',
                state=DeleteEditOrder.update_course
            ),
            width=2,
            id='order_events_row'
        ),
        Button(Const("❌ Отмена"), id="start_bot", on_click=start),
        getter=order_getter,
        state=DeleteEditOrder.update_menu
    )


def update_min_sum_order() -> Window:
    return Window(
        Const('Введите новую минимальную сумму'),
        TextInput(
            id='min_sum_input',
            type_factory=float,
            on_success=update_min_sum,
            on_error=error_handler
        ),
        Button(Const("❌ Отмена"), id="start_bot", on_click=start),
        state=DeleteEditOrder.update_min_sum
    )


def update_max_sum_order() -> Window:
    return Window(
        Const('Введите новую максимальную сумму'),
        TextInput(
            id='max_sum_input',
            type_factory=float,
            on_success=update_max_sum,
            on_error=error_handler,
        ),
        Button(Const("❌ Отмена"), id="start_bot", on_click=start),
        state=DeleteEditOrder.update_max_sum
    )


def update_cource_order() -> Window:
    return Window(
        Format(
            "Укажите желаемую стоимость PRIZM в рублях.\nТекущий курс <b>{prizm_rate}</b> PZM/RUB "
            "https://coinmarketcap.com/currencies/prizm .\nРазница указанного вами курса не должна отличаться "
            "более чем на {prizm_rate_diff_percent}%"),
        TextInput(
            id='new_cource',
            type_factory=float,
            on_success=update_cource,
            on_error=error_handler,
        ),
        Button(Const("❌ Отмена"), id="start_bot", on_click=start),
        getter=get_prizm_rate,
        state=DeleteEditOrder.update_course
    )