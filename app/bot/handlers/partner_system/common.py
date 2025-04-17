from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.handlers.partner_system.states import UpdateChannel
from app.bot.ui.partner_system import withdraw_partner_balance, owners_menu
from app.bot.utils.parce import get_partner_data
from app.core.models import User

router = Router()


@router.callback_query(F.data == 'partner_system')
async def ask_how_many(callback: CallbackQuery, bot: Bot, session: AsyncSession, user_db: User):
    me = await bot.get_me()
    link = f'https://t.me/{me.username}' + '?start=' + hex(callback.from_user.id)

    data = await get_partner_data(session, callback.from_user.id)

    count_users = data.get('count_users', None)

    if count_users:
        text = (f'Всего приглашенных: {count_users}\n'
                f'Их суммарный оборот: {data["summ"]:.3f} PZM\n'
                f'Ваш реферальный баланс: {user_db.referral_balance:.3f} PZM')
    else:
        text = 'У вас пока нет приглашенных пользователей'

    await callback.message.answer("Приглашайте новых пользователей и получайте 10% от комиссии "
                                  "нашего бота с оборота всех привлеченных вами клиентов.\n\n"
                                  f"Ваша ссылка (👇нажми):\n<code>{link}</code>\n\n{text}",
                                  reply_markup=withdraw_partner_balance,
                                  parse_mode='html')


@router.callback_query(F.data == 'group_channel_owners')
async def group_channel_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(
        'Наш бот может публиковать самые выгодные ордера на покупку и продажу PZM в вашей группе или канале, а также текущий курс на Coinmarketcap. В сообщении будет указана Ваша реферальная ссылка для перехода в наш бот. Таким образом Ваши подписчики будут переходить в бота по Вашей реферальной ссылке, а вы будете получать вознаграждение от нашего бота: 10% от прибыли с привлеченных Вами пользователей.\n\nСделайте это всего лишь в 3 шага:\n\n',
        reply_markup=owners_menu
    )


@router.callback_query(F.data == 'my_channels')
async def my_chats(callback: CallbackQuery, session: AsyncSession, dialog_manager: DialogManager):
    await dialog_manager.start(UpdateChannel.select_chat)
