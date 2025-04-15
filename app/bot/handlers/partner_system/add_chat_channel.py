from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ChatMemberAdministrator
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.handlers.partner_system.states import AddChannel
from app.bot.ui.partner_system import cancel_partner_system, accept_add_bot
from app.core.dao import crud_chat_channel
from app.core.dto import ChatChannelCreate
from app.utils.text_check import check_interval

router = Router()


@router.callback_query(F.data == 'add_channel')
async def group_channel_menu(callback: CallbackQuery, state: FSMContext, session: AsyncSession, bot: Bot):
    await callback.message.answer(
        'Наш бот может публиковать самые выгодные ордера на покупку и продажу PZM в вашей группе или '
        'канале, а также текущий курс на Coinmarketcap. В сообщении будет указана Ваша реферальная '
        'ссылка для перехода в наш бот. Таким образом Ваши подписчики будут переходить в бота по Вашей '
        'реферальной ссылке. \n\nСделайте это всего лишь в 3 шага:\n\n'
        f'1. Добавьте нашего бота {(await bot.get_me()).url} в администраторы своей группы/канала\n\n'  # ссылку получить
        '2. Отправьте нам айди группы/канала. Это можно сделать в данном боте: @username_to_id_bot',
        reply_markup=cancel_partner_system)
    await state.set_state(AddChannel.get_chat_channel_id)


@router.message(AddChannel.get_chat_channel_id, F.text)
async def save_link(message: Message, state: FSMContext, bot: Bot):
    if message.text[0] != '-' or not message.text[1:].isdigit():
        await message.answer('Отправьте, пожалуйста, корректный айди', reply_markup=cancel_partner_system)
        return

    await state.update_data(chat_channel_id=int(message.text))
    await state.set_state(AddChannel.accept)
    await message.answer('Текст', reply_markup=accept_add_bot)  # todo


@router.callback_query(F.data == 'add_bot', AddChannel.accept)
async def accept_add_bot_handler(callback: CallbackQuery, state: FSMContext, bot: Bot):
    try:
        assert isinstance(await bot.get_chat_member(await state.get_value('chat_channel_id'), bot.id),
                          ChatMemberAdministrator)
    except:
        await callback.message.answer('Добавьте бота в администраторы', reply_markup=accept_add_bot)
        return

    await state.set_state(AddChannel.get_count_in_day)
    await callback.message.answer('Сколько раз в день должен выходить пост?', reply_markup=cancel_partner_system)


@router.message(AddChannel.get_count_in_day)
async def save_count(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Отправьте, пожалуйста, корректное число', reply_markup=cancel_partner_system)
        return

    await state.set_state(AddChannel.get_interval)
    await state.update_data(count_in_day=int(message.text))
    await message.answer('Как часто в минутах должен выходить пост?', reply_markup=cancel_partner_system)


@router.message(AddChannel.get_interval)
async def save_count(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Отправьте, пожалуйста, корректное число', reply_markup=cancel_partner_system)
        return

    await state.update_data(interval=int(message.text))
    await state.set_state(AddChannel.get_interval_in_day)
    await message.answer('Укажите интервал по мск (в формате 09:00-21:00)', reply_markup=cancel_partner_system)


@router.message(AddChannel.get_interval_in_day)
async def save_count(message: Message, state: FSMContext, session: AsyncSession):
    if not check_interval(message.text):
        await message.answer('Отправьте, пожалуйста, корректный интервал (в формате 09:00-21:00)',
                             reply_markup=cancel_partner_system)
        return

    chat_channel_id = await state.get_value('chat_channel_id')
    count_in_day = await state.get_value('count_in_day')
    interval = await state.get_value('interval')
    interval_in_day = message.text
    create_chat_channel = ChatChannelCreate(user_id=message.from_user.id,
                                            id=chat_channel_id,
                                            count_in_day=count_in_day,
                                            interval=interval,
                                            is_bot_admin=True,
                                            interval_in_day=interval_in_day
                                            )

    await crud_chat_channel.create(session, obj_in=create_chat_channel)
    await state.clear()
    await message.answer('🎉 Поздравляем, Ваша группа/канал добавлена')
