from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.handlers.partner_system.states import UpdateChannel
from app.bot.ui import get_menu_kb
from app.bot.ui.partner_system import cancel_partner_system, update_chats, update_chat_options, cancel_to_my_channels
from app.core.dao import crud_chat_channel
from app.core.models import User
from app.utils.text_check import check_interval

router = Router()


@router.callback_query(F.data == 'my_channels')
async def my_chats(callback: CallbackQuery, session: AsyncSession):
    chats = await crud_chat_channel.get_by_user_id(session, user_id=callback.from_user.id)
    if not chats:
        await callback.message.answer('У вас нет чатов', reply_markup=cancel_partner_system)
        return

    text = ''

    for chat in chats:
        text += f'{chat.username or chat.name or chat.id}\n'

    await callback.message.answer(f'Ваши чаты:\n{text}', reply_markup=update_chats(chats))


@router.callback_query(F.data.startswith('update_'))
async def my_chats(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    chat_id = int(callback.data.split('_')[1])
    chat = await crud_chat_channel.get_by_id(session, id=chat_id)

    await state.set_state(UpdateChannel.select_option)
    await state.update_data(chat_id=chat_id)

    text = (f'ID чата: {chat.id}\n' +
            (f'Username: @{chat.username}\n' if chat.username else '') +
            (f'Название: {chat.name}\n' if chat.name else '') +
            f'Кол-во в день: {chat.count_in_day}\n'
            f'Время между постами: {chat.interval}\n'
            f'Интервал в течение дня: {chat.interval_in_day}.\n\n'
            f'Выберите, что вы хотите изменить:')

    await callback.message.answer(text, reply_markup=update_chat_options)


@router.callback_query(F.data.in_(['count_in_day', 'interval', 'interval_in_day']), UpdateChannel.select_option)
async def wait_new_value(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    # chat_id = await state.get_value('chat_id')
    # chat = await crud_chat_channel.get_by_id(session, id=chat_id)

    await state.set_state(UpdateChannel.get_new_value)
    await state.update_data(option=callback.data)

    if callback.data == 'interval_in_day':
        await callback.message.answer('Введите интервал в течение дня (в формате 09:00-21:00)',
                                      reply_markup=cancel_to_my_channels)
        return

    await callback.message.answer('Введите новое значение', reply_markup=cancel_to_my_channels)


@router.message(UpdateChannel.get_new_value)
async def wait_new_value(message: Message, session: AsyncSession, state: FSMContext, user_db: User):
    chat_id = await state.get_value('chat_id')
    chat = await crud_chat_channel.get_by_id(session, id=chat_id)
    option = await state.get_value('option')
    if option in ['count_in_day', 'interval']:
        if not message.text.isdigit():
            await message.answer('Введите число', reply_markup=cancel_to_my_channels)
            return
        value = int(message.text)
    elif option == 'interval_in_day':
        if not check_interval(message.text):
            await message.answer('Отправьте, пожалуйста, корректный интервал (в формате 09:00-21:00)',
                                 reply_markup=cancel_to_my_channels)
            return
        value = message.text

    chat = await crud_chat_channel.update(session, obj_in={'id': chat_id, option: value})

    text = (f'ID чата: {chat.id}\n'
            f'Username: {chat.username}\n' if chat.username else ''
                                                                 f'Название: {chat.name}\n' if chat.name else ''
                                                                                                              f'Колво в день: {chat.count_in_day}\n'
                                                                                                              f'Время между постами: {chat.interval}\n'
                                                                                                              f'Интервал в течение дня: {chat.interval_in_day}.\n\n'
                                                                                                              f'Выберите, что вы хотите изменить:')

    await state.set_state(UpdateChannel.select_option)
    await message.answer(text, reply_markup=update_chat_options)
