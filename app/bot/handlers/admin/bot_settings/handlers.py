from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import ManagedTextInput

from app.bot.handlers.common import start_cmd_cb
from app.bot.ui import admin_panel_commot_kb
from app.core.dao import crud_settings, crud_user
from app.core.models import User


async def cancel_logic(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await callback.message.answer("Вы отменили создание ордера")
    await dialog_manager.done()
    await start_cmd_cb(callback, callback.bot, dialog_manager.middleware_data['state'],
                       dialog_manager.middleware_data['user_db'], dialog_manager,
                       dialog_manager.middleware_data['session'])


async def on_back(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.back(show_mode=ShowMode.DELETE_AND_SEND)


async def on_new_wait_order_time(message: Message, text_widget: ManagedTextInput, dialog_manager: DialogManager, data):
    new_value = text_widget.get_value()
    await crud_settings.update(dialog_manager.middleware_data['session'],
                               obj_in={"id": 1, "order_wait_minutes": new_value})
    user_db = dialog_manager.middleware_data['user_db']
    await message.answer("Ваши изменения применены", reply_markup=admin_panel_commot_kb(user_db.role == User.MAIN_ADMIN))
    await dialog_manager.done(show_mode=ShowMode.DELETE_AND_SEND)


async def on_new_commission_percent_value(message: Message, text_widget: ManagedTextInput,
                                          dialog_manager: DialogManager, data):
    new_value = text_widget.get_value()
    await crud_settings.update(dialog_manager.middleware_data['session'],
                               obj_in={"id": 1, "commission_percent": new_value / 100})
    user_db = dialog_manager.middleware_data['user_db']
    await message.answer("Ваши изменения применены", reply_markup=admin_panel_commot_kb(user_db.role == User.MAIN_ADMIN))
    await dialog_manager.done(show_mode=ShowMode.DELETE_AND_SEND)


async def on_new_withdrawal_commission_percent_value(message: Message, text_widget: ManagedTextInput,
                                                     dialog_manager: DialogManager, data):
    new_value = text_widget.get_value()
    await crud_settings.update(dialog_manager.middleware_data['session'],
                               obj_in={"id": 1, "withdrawal_commission_percent": new_value / 100})
    user_db = dialog_manager.middleware_data['user_db']
    await message.answer("Ваши изменения применены", reply_markup=admin_panel_commot_kb(user_db.role == User.MAIN_ADMIN))
    await dialog_manager.done(show_mode=ShowMode.DELETE_AND_SEND)

async def on_new_min_order_prizm_value(message: Message, text_widget: ManagedTextInput,
                                                     dialog_manager: DialogManager, data):
    new_value = text_widget.get_value()
    await crud_settings.update(dialog_manager.middleware_data['session'],
                               obj_in={"id": 1, "min_order_prizm_value": new_value})
    user_db = dialog_manager.middleware_data['user_db']
    await message.answer("Ваши изменения применены", reply_markup=admin_panel_commot_kb(user_db.role == User.MAIN_ADMIN))
    await dialog_manager.done(show_mode=ShowMode.DELETE_AND_SEND)



async def on_new_referal_withdrawal_minimum_value(message: Message, text_widget: ManagedTextInput,
                                                     dialog_manager: DialogManager, data):
    new_value = text_widget.get_value()
    await crud_settings.update(dialog_manager.middleware_data['session'],
                               obj_in={"id": 1, "minimum_referal_withdrawal_amount": new_value})
    user_db = dialog_manager.middleware_data['user_db']
    await message.answer("Ваши изменения применены", reply_markup=admin_panel_commot_kb(user_db.role == User.MAIN_ADMIN))
    await dialog_manager.done(show_mode=ShowMode.DELETE_AND_SEND)


async def on_pay_order_time_value(message: Message, text_widget: ManagedTextInput,
                                  dialog_manager: DialogManager, data):
    new_value = text_widget.get_value()
    await crud_settings.update(dialog_manager.middleware_data['session'], obj_in={"id": 1, "pay_wait_time": new_value})
    user_db = dialog_manager.middleware_data['user_db']
    await message.answer("Ваши изменения применены", reply_markup=admin_panel_commot_kb(user_db.role == User.MAIN_ADMIN))
    await dialog_manager.done(show_mode=ShowMode.DELETE_AND_SEND)


async def on_prizm_rate_diff_value(message: Message, text_widget: ManagedTextInput,
                                   dialog_manager: DialogManager, data):
    new_value = text_widget.get_value()
    await crud_settings.update(dialog_manager.middleware_data['session'],
                               obj_in={"id": 1, "prizm_rate_diff": new_value / 100})
    user_db = dialog_manager.middleware_data['user_db']
    await message.answer("Ваши изменения применены", reply_markup=admin_panel_commot_kb(user_db.role == User.MAIN_ADMIN))
    await dialog_manager.done(show_mode=ShowMode.DELETE_AND_SEND)


async def on_add_admin_username_value(message: Message, text_widget: ManagedTextInput,
                                      dialog_manager: DialogManager, data):
    user_db = dialog_manager.middleware_data['user_db']
    if user_db.role != User.MAIN_ADMIN:
        await message.answer(f"Вы не можете добавлять админа!",
                             reply_markup=admin_panel_commot_kb(user_db.role == User.MAIN_ADMIN))
        return
    new_value = text_widget.get_value()
    session = dialog_manager.middleware_data['session']
    user_by_username = await crud_user.get_by_username(session, username=new_value)
    if not user_by_username:
        await message.answer("Пользователь не найден")
        return
    await crud_user.update(session, db_obj=user_by_username, obj_in={"role": User.ADMIN_ROLE})

    await message.answer(f"Ваши изменения применены. {new_value} админ", reply_markup=admin_panel_commot_kb(user_db.role == User.MAIN_ADMIN))
    await dialog_manager.done(show_mode=ShowMode.DELETE_AND_SEND)


async def on_remove_admin_username_value(message: Message, text_widget: ManagedTextInput,
                                         dialog_manager: DialogManager, data):
    user_db = dialog_manager.middleware_data['user_db']
    if user_db.role != User.MAIN_ADMIN:
        await message.answer(f"Вы не можете удалять админа!",
                             reply_markup=admin_panel_commot_kb(user_db.role == User.MAIN_ADMIN))
        return
    new_value = text_widget.get_value()
    session = dialog_manager.middleware_data['session']
    user_by_username = await crud_user.get_by_username(session, username=new_value)
    if not user_by_username:
        await message.answer("Пользователь не найден")
        return
    await crud_user.update(session, db_obj=user_by_username, obj_in={"role": User.USER_ROLE})
    await message.answer(f"Ваши изменения применены. {new_value} не админ", reply_markup=admin_panel_commot_kb(user_db.role == User.MAIN_ADMIN))
    await dialog_manager.done(show_mode=ShowMode.DELETE_AND_SEND)
