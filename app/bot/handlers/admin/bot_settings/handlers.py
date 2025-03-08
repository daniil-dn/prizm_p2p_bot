from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import ManagedTextInput

from app.bot.handlers.common import start_cmd
from app.bot.ui import admin_panel_commot_kb
from app.core.dao import crud_settings


async def cancel_logic(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await callback.message.answer("Вы отменили создание ордера")
    await dialog_manager.done()
    await start_cmd(callback.message, callback.bot, dialog_manager.middleware_data['state'],
                    dialog_manager.middleware_data['user_db'], dialog_manager)


async def on_back(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.back(show_mode=ShowMode.DELETE_AND_SEND)


async def on_new_wait_order_time(message: Message, text_widget: ManagedTextInput, dialog_manager: DialogManager, data):
    new_value = text_widget.get_value()
    async with dialog_manager.middleware_data['session'] as session:
        await crud_settings.update(session, obj_in={"id": 1, "order_wait_minutes": new_value})
    await message.answer("Ваши изменения применены", reply_markup=admin_panel_commot_kb())
    await dialog_manager.done(show_mode=ShowMode.DELETE_AND_SEND)


async def on_new_commission_percent_value(message: Message, text_widget: ManagedTextInput,
                                          dialog_manager: DialogManager, data):
    new_value = text_widget.get_value()
    async with dialog_manager.middleware_data['session'] as session:
        await crud_settings.update(session, obj_in={"id": 1, "commission_percent": new_value / 100})
    await message.answer("Ваши изменения применены", reply_markup=admin_panel_commot_kb())
    await dialog_manager.done(show_mode=ShowMode.DELETE_AND_SEND)


async def on_pay_order_time_value(message: Message, text_widget: ManagedTextInput,
                                  dialog_manager: DialogManager, data):
    new_value = text_widget.get_value()
    async with dialog_manager.middleware_data['session'] as session:
        await crud_settings.update(session, obj_in={"id": 1, "pay_wait_time": new_value})
    await message.answer("Ваши изменения применены", reply_markup=admin_panel_commot_kb())
    await dialog_manager.done(show_mode=ShowMode.DELETE_AND_SEND)


async def on_prizm_rate_diff_value(message: Message, text_widget: ManagedTextInput,
                                   dialog_manager: DialogManager, data):
    new_value = text_widget.get_value()
    async with dialog_manager.middleware_data['session'] as session:
        await crud_settings.update(session, obj_in={"id": 1, "prizm_rate_diff": new_value / 100})
    await message.answer("Ваши изменения применены", reply_markup=admin_panel_commot_kb())
    await dialog_manager.done(show_mode=ShowMode.DELETE_AND_SEND)
