import asyncio

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.handlers.partner_system.states import WithdrawPartner
from app.bot.ui import get_menu_kb
from app.bot.ui.partner_system import admin_withdrawal_done
from app.bot.ui.withdraw import cancel_withdraw
from app.bot.utils.parce import get_partner_data
from app.core.dao import crud_user, crud_settings
from app.core.dao.crud_withdraw_ref import crud_withdraw_ref
from app.core.dto.withdraw_ref import WithdrawRefCreate
from app.core.models import User
from app.utils.text_check import check_wallet_format

router = Router()


@router.callback_query(F.data == 'withdraw_partner_balance')
async def get_summ_to_output(callback: CallbackQuery, state: FSMContext, user_db: User, session: AsyncSession):
    admin_settings = await crud_settings.get_by_id(session, id=1)
    if user_db.referral_balance < admin_settings.minimum_referal_withdrawal_amount:
        await callback.answer('Вывод доступен только от тысячи prizm', show_alert=True)
        return

    await state.set_state(WithdrawPartner.get_count_money)
    await callback.message.answer('Введите сумму для вывода. Обращаем ваше внимание, вывод будет осуществлен '
                                  'в течение 24 часов, и минимальная сумма, доступная к выводу - 1000 prizm')


@router.message(WithdrawPartner.get_count_money)
async def check_input_and_ask_address(message: Message, state: FSMContext, user_db: User, session: AsyncSession):
    try:
        amount = float(message.text)
    except:
        await message.answer('Сумма должна быть числом. Попробуйте снова', reply_markup=cancel_withdraw)
        return
    admin_settings = await crud_settings.get_by_id(session, id=1)
    if amount > user_db.referral_balance or amount < admin_settings.minimum_referal_withdrawal_amount:
        await message.answer('Введите корректную сумму больше 1000', reply_markup=cancel_withdraw)
        return

    await state.set_data({'amount': amount})
    await state.set_state(WithdrawPartner.get_prizm_address)

    await message.answer('Отправьте адрес кошелька в таком формате: PRIZM-****-****-****-****',
                         reply_markup=cancel_withdraw)


@router.message(WithdrawPartner.get_prizm_address)
async def check_input_and_withdraw_balance(message: Message, state: FSMContext,
                                           session: AsyncSession, bot: Bot, user_db: User):
    if not check_wallet_format(message.text):
        await message.answer('Отправьте адрес кошелька в таком формате: PRIZM-****-****-****-****',
                             reply_markup=cancel_withdraw)
        return

    amount = await state.get_value('amount')
    main_admins = await crud_user.get_main_admins(session)

    data = await get_partner_data(session, message.from_user.id)

    data = await get_partner_data(session, message.from_user.id)

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


    withdraw_create = WithdrawRefCreate(user_id=message.from_user.id, summ=amount)
    await crud_withdraw_ref.create(session, obj_in=withdraw_create)
    await crud_user.decrease_referral_balance(session, id=message.from_user.id, summ=amount)

    try:
        await message.answer('Деньги будут выведены на указанный адрес')
        for main_admin in main_admins:
            await bot.send_message(main_admin.id, text=f'Количество монет на вывод: {amount} pzm\n'
                                                       f'User: @{message.from_user.username} ({message.from_user.id})\n'
                                                       f'Процент комиссии {percent * 100:.1f}\n\n'
                                                       f'{text}'
                                                       f'Баланс пользователя: {user_db.referral_balance:.3f} PZM\n'
                                                       f'Кошелек: {message.text}')

            await bot.send_message(main_admin.id, text=f'{message.text}',
                                   reply_markup=admin_withdrawal_done(message.from_user.id))
            await asyncio.sleep(0.5)
    except:
        await message.answer('Возникла ошибка, напишите в поддержку')
    await state.clear()


@router.callback_query(F.data.startswith('admin-done-partner-withdraw-request'))
async def admin_done_order(callback: CallbackQuery, state: FSMContext, user_db: User, session: AsyncSession):
    user_id = callback.data.split('_')[1]
    client_user_db = await crud_user.get_by_id(session, id=int(user_id))
    await callback.bot.send_message(user_id, '💰Ваша заявка обработана. Монеты переведены на указанный вами кошелек.')
    await callback.message.edit_reply_markup(None)
    await callback.message.reply('✅Пользователь уведомлен!',
                                 reply_markup=get_menu_kb(is_admin=user_db.role in User.ALL_ADMINS))