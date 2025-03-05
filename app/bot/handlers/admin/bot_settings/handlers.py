from datetime import date
from decimal import Decimal

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import ManagedTextInput
from redis.utils import dict_merge

from app.bot.handlers.new_order.state import NewOrderState
from app.bot.handlers.common import start_cmd
from app.bot.ui import order_seller_accept_kb
from app.core.config import settings
from app.core.dao import crud_order_request, crud_order, crud_settings
from app.core.dao.crud_wallet import crud_wallet
from app.core.dto import OrderCreate, WalletCreate, OrderRequestCreate
from app.core.models import OrderRequest, Order
from app.utils.coinmarketcap import get_currency_rate, rate_difference


async def cancel_logic(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await callback.message.answer("Вы отменили создание ордера")
    await dialog_manager.done()
    await start_cmd(callback.message, callback.bot, dialog_manager.middleware_data['state'],
                    dialog_manager.middleware_data['user_db'])


async def on_back(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.back(show_mode=ShowMode.DELETE_AND_SEND)


async def on_new_wait_order_time(message: Message, text_widget: ManagedTextInput, dialog_manager: DialogManager, data):
    """Обработчик выбора количества гостей."""
    new_value = text_widget.get_value()
    async with dialog_manager.middleware_data['session'] as session:
        await crud_settings.update(session, obj_in={"id": 1, "order_wait_minutes": new_value})
    await message.answer("Ваши изменения применены")
    await dialog_manager.done(show_mode=ShowMode.DELETE_AND_SEND)


async def on_new_commission_percent_value(message: Message, text_widget: ManagedTextInput,
                                          dialog_manager: DialogManager, data):
    """Обработчик выбора количества гостей."""
    new_value = text_widget.get_value()
    async with dialog_manager.middleware_data['session'] as session:
        await crud_settings.update(session, obj_in={"id": 1, "commission_percent": new_value})
    await message.answer("Ваши изменения применены")
    await dialog_manager.done(show_mode=ShowMode.DELETE_AND_SEND)


async def on_pay_order_time_value(message: Message, text_widget: ManagedTextInput,
                                  dialog_manager: DialogManager, data):
    """Обработчик выбора количества гостей."""
    new_value = text_widget.get_value()
    async with dialog_manager.middleware_data['session'] as session:
        await crud_settings.update(session, obj_in={"id": 1, "pay_wait_time": new_value})
    await message.answer("Ваши изменения применены")
    await dialog_manager.done(show_mode=ShowMode.DELETE_AND_SEND)
