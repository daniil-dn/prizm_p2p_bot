from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.handlers.menu.states import WithdrawPartner
from app.bot.ui.partner_system import withdraw_partner_balance
from app.bot.ui.withdraw import cancel_withdraw
from app.bot.utils.parce import get_partner_data
from app.core.dao import crud_user, crud_settings
from app.core.dao.crud_withdraw_ref import crud_withdraw_ref
from app.core.dto.withdraw_ref import WithdrawRefCreate
from app.core.models import User
from app.utils.text_check import check_wallet_format

router = Router()


@router.callback_query(F.data == 'partner_system')
async def ask_how_many(callback: CallbackQuery, bot: Bot, session: AsyncSession):
    me = await bot.get_me()
    link = f'https://t.me/{me.username}' + '?start=' + hex(callback.from_user.id)

    data = await get_partner_data(session, callback.from_user.id)

    summ = data.get('summ', None)
    count_users = data.get('count_users', None)
    count_orders = data.get('count_orders', None)
    commission = data.get('commission', None)
    percent = data.get('percent', None)

    if count_users:
        text = (f'Всего приглашенных: {count_users}\n'
                f'Проведено сделок: {count_orders}\n'
                f'Общая сумма сделок: {summ} призм\n'
                f'Ваша комиссия ({int(percent * 100)}% от комиссии бота): '
                f'{commission} призм')
    else:
        text = 'У вас пока нет приглашенных пользователей'

    await callback.message.answer("Приглашайте новых пользователей и получайте 10% от комиссии "
                                  "нашего бота с оборота всех привлеченных вами клиентов.\n\n"
                                  f"Ваша ссылка: {link}\n\n{text}", reply_markup=withdraw_partner_balance)


@router.callback_query(F.data == 'withdraw_partner_balance')
async def get_summ_to_output(callback: CallbackQuery, state: FSMContext, user_db: User, session: AsyncSession):
    data = await get_partner_data(session, callback.from_user.id)
    summ = data.get('summ', None)

    if summ < 1000:
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

    data = await get_partner_data(session, message.from_user.id)
    summ = data.get('summ', None)

    if amount > summ or amount < 1000:
        await message.answer('Введите корректную сумму больше 1000', reply_markup=cancel_withdraw)
        return

    await state.set_data({'amount': amount})
    await state.set_state(WithdrawPartner.get_prizm_address)

    await message.answer('Отправьте адрес кошелька в таком формате: PRIZM-****-****-****-****',
                         reply_markup=cancel_withdraw)


@router.message(WithdrawPartner.get_prizm_address)
async def check_input_and_withdraw_balance(message: Message, state: FSMContext,
                                           session: AsyncSession, bot: Bot):
    if not check_wallet_format(message.text):
        await message.answer('Отправьте адрес кошелька в таком формате: PRIZM-****-****-****-****',
                             reply_markup=cancel_withdraw)
        return
    await state.clear()

    amount = await state.get_value('amount')
    main_admin = await crud_user.get_main_admin(session)

    data = await get_partner_data(session, message.from_user.id)

    summ = data.get('summ', None)
    count_users = data.get('count_users', None)
    count_orders = data.get('count_orders', None)
    commission = data.get('commission', None)
    percent = data.get('percent', None)

    withdraw_create = WithdrawRefCreate(user_id=message.from_user.id, summ=amount)
    await crud_withdraw_ref.create(session, obj_in=withdraw_create)

    try:
        await message.answer('Деньги будут выведены на указанный адрес')
        await bot.send_message(main_admin.id, text=f'Количество: {amount}\n'
                                                   f'user: @{message.from_user.username} ({message.from_user.id})\n'
                                                   f'Кол-во приглашенных {count_users}\n'
                                                   f'Проведено сделок: {count_orders}\n'
                                                   f'Общая сумма сделок: {summ} призм\n'
                                                   f'Процент пользователя {commission}')
    except:
        await message.answer('Возникла ошибка, напишите в поддержку')
