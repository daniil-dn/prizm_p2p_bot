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

    descendants_result = data.get('descendants_result', None)
    partner_commissions = [0.06, 0.03, 0.01]
    percent = data.get('percent', None)
    text = ""
    for user_level in range(3):
        users_by_level = descendants_result[user_level]
        text += (
            f"{user_level + 1} уровень ({int(partner_commissions[user_level] * 100)}%) - {users_by_level['user_count']} чел\n"
            f"Оборот: {users_by_level['summ']} pzm\n"
            f"Комиссия бота: {users_by_level['bot_commission_summ']} pzm \n"
            f"Ваша комиссия: {users_by_level['partner_level_commission_summ']} pzm\n\n")

    await callback.message.answer(
        "Приглашайте новых пользователей и получайте 6% от комиссии нашего бота с оборота всех привлеченных вами клиентов + 3% с оборота тех, кого они пригласили и 1% с рефрералов третьего уровня.\n\n"
        f"Ваша ссылка (👇нажми):\n<code>{link}</code>\n\n{text}"
        f"Ваш реферальный баланс: {user_db.referral_balance} pzm\n",
        reply_markup=withdraw_partner_balance,
        parse_mode='html')


@router.callback_query(F.data == 'group_channel_owners')
async def group_channel_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(
        'Наш бот может публиковать самые выгодные ордера на покупку и продажу PZM в вашей группе или канале, а также текущий курс на <a href="https://coinmarketcap.com/currencies/prizm">🔗Coinmarketcap</a>.\nВ сообщении будет указана Ваша реферальная ссылка для перехода в наш бот. Таким образом Ваши подписчики будут переходить в бота по Вашей реферальной ссылке, а вы будете получать 6% от комиссии нашего бота с оборота всех привлеченных вами клиентов + 3% с оборота тех, кого они пригласили и 1% с рефрералов третьего уровня.\n\nСделайте это всего лишь в 3 шага:\n\n',
        reply_markup=owners_menu, parse_mode='html', disable_web_page_preview=True
    )


@router.callback_query(F.data == 'my_channels')
async def my_chats(callback: CallbackQuery, session: AsyncSession, dialog_manager: DialogManager):
    await dialog_manager.start(UpdateChannel.select_chat)
