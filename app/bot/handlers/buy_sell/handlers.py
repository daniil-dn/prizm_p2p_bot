from datetime import date
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import ManagedTextInput

from app.bot.handlers.buy_sell.state import BuyState
from app.bot.ui import get_menu_kb


async def cancel_logic(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await callback.message.answer("Вы отменили поиск ордеров",
                                  reply_markup=get_menu_kb())


async def on_value_selected(message: Message, text_widget: ManagedTextInput, dialog_manager: DialogManager, data):
    """Обработчик выбора количества гостей."""
    if dialog_manager.start_data['mode'] == 'sell':
        await dialog_manager.switch_to(state=BuyState.orders_list, show_mode=ShowMode.DELETE_AND_SEND)
    else:
        await dialog_manager.next()


async def process_order_request_selected(callback: CallbackQuery, widget, dialog_manager: DialogManager, item_id: str):
    return

async def on_orders_page_changed( *args, **kwargs):
    return