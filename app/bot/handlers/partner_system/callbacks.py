from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button

from app.bot.handlers.partner_system.states import UpdateChannel
from app.bot.ui.partner_system import owners_menu
from app.core.dao import crud_chat_channel


async def back_to_partner(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.done()
    await callback.message.answer(
        'Выберите пункт меню',
        reply_markup=owners_menu
    )


async def select_chat(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, data):
    dialog_manager.dialog_data['selected_chat'] = data
    await dialog_manager.switch_to(UpdateChannel.select_option)


async def stop_chat(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    chat_id = int(dialog_manager.dialog_data['selected_chat'])
    chat = await crud_chat_channel.update(dialog_manager.middleware_data['session'],
                                          obj_in={'id': chat_id, 'is_stopped': True})


async def update_count(message: Message, text_widget: ManagedTextInput, dialog_manager: DialogManager, text):
    chat_id = int(dialog_manager.dialog_data['selected_chat'])
    chat = await crud_chat_channel.update(dialog_manager.middleware_data['session'],
                                          obj_in={'id': chat_id, 'count_in_day': int(text)})
    await dialog_manager.switch_to(UpdateChannel.select_option)


async def update_interval(message: Message, text_widget: ManagedTextInput, dialog_manager: DialogManager, text):
    chat_id = int(dialog_manager.dialog_data['selected_chat'])
    chat = await crud_chat_channel.update(dialog_manager.middleware_data['session'],
                                          obj_in={'id': chat_id, 'interval': int(text)})
    await dialog_manager.switch_to(UpdateChannel.select_option)


async def update_interval_in_day(message: Message, text_widget: ManagedTextInput, dialog_manager: DialogManager, text):
    chat_id = int(dialog_manager.dialog_data['selected_chat'])
    chat = await crud_chat_channel.update(dialog_manager.middleware_data['session'],
                                          obj_in={'id': chat_id, 'interval_in_day': text})
    await dialog_manager.switch_to(UpdateChannel.select_option)


async def continue_chat(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    chat_id = int(dialog_manager.dialog_data['selected_chat'])
    chat = await crud_chat_channel.update(dialog_manager.middleware_data['session'],
                                          obj_in={'id': chat_id, 'is_stopped': False})


async def error_number(
        message: Message,
        dialog_,
        manager: DialogManager,
        error_: ValueError
):
    await message.answer('Введите число')


async def error_interval(
        message: Message,
        dialog_,
        manager: DialogManager,
        error_: ValueError
):
    await message.answer('Отправьте, пожалуйста, корректный интервал (в формате 09:00-21:00)')
