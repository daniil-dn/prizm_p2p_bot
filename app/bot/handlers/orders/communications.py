from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.handlers.orders.state import GetMessage
from app.bot.ui.order_seller_accept import contact_to_user, cancel_contact, contact_to_user_and_back
from app.core.dao import crud_user, crud_order
from app.core.dao.crud_message import crud_message
from app.core.dto import MessageCreate

router = Router()


@router.callback_query(F.data.startswith('contact_'))
async def ask_message_to_send(callback: CallbackQuery, state: FSMContext):
    await state.set_state(GetMessage.wait_for_message)
    to_user_id = int(callback.data.split('_')[1])
    order_id = int(callback.data.split('_')[2])
    await state.set_data({'to_user_id': to_user_id, 'order_id': order_id})
    await callback.message.answer('Введите сообщения для пользователя (можно отправить 1 фото или 1 документ)',
                                  reply_markup=cancel_contact)
    await callback.answer()


@router.callback_query(F.data == 'cancel_contact')
async def ask_message_to_send(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    try:
        await callback.message.delete()
    except:
        pass
    await callback.message.answer('Отменено')
    await callback.answer()


@router.message(GetMessage.wait_for_message)
async def send_message_to_user(message: Message, state: FSMContext, bot: Bot, session: AsyncSession):
    to_user_tg_id = await state.get_value('to_user_id')

    order_id = await state.get_value('order_id')
    async with session:
        order = await crud_order.get_by_id(session, id=order_id)
    await state.clear()

    document = None
    photo = None
    if message.photo:
        photo = message.photo[-1].file_id
    elif message.document:
        document = message.document.file_id
    try:
        await message.copy_to(to_user_tg_id,
                              reply_markup=contact_to_user_and_back(message.from_user.id, order))
        await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id - 1)
    except:
        pass
    await message.answer('Сообщение отправлено',
                         reply_markup=contact_to_user_and_back(to_user_tg_id, order))
    async with session:
        to_user = await crud_user.get(session, to_user_tg_id)
        from_user = await crud_user.get(session, message.from_user.id)

        message_to_create = MessageCreate(from_user_id=from_user.id, to_user_id=to_user.id, photo=photo,
                                          document=document, text=message.text or message.caption, order_id=order_id)
        await crud_message.create(session, obj_in=message_to_create)
