from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.handlers.menu.states import Withdraw
from app.bot.ui import get_menu_kb
from app.bot.ui.menu import menu_button
from app.bot.ui.texts import get_start_text
from app.bot.ui.withdraw import cancel_withdraw
from app.core.config import settings
from app.core.dao import crud_user, crud_settings
from app.core.models import User
from app.prizm_check_scheduler.prizm_fetcher import PrizmWalletFetcher
from app.utils.text_check import check_wallet_format

router = Router()


@router.callback_query(F.data == 'withdraw_balance')
async def ask_how_many(callback: CallbackQuery, state: FSMContext, user_db: User, session: AsyncSession):
    await state.set_state(Withdraw.get_count_money)
    admin_settings = await crud_settings.get_by_id(session, id=1)
    await callback.message.answer(
        f'Введите сумму для вывода. Ваш текущий баланс: {user_db.balance}.\nКомиссия сервиса {admin_settings.commission_percent * 100}%',
        reply_markup=cancel_withdraw)


@router.message(Withdraw.get_count_money)
async def check_input_and_ask_address(message: Message, state: FSMContext, user_db: User, session: AsyncSession):
    try:
        amount = float(message.text)
    except:
        await message.answer('Сумма должна быть числом. Попробуйте снова', reply_markup=cancel_withdraw)
        return

    if amount > user_db.balance or amount <= 0:
        await message.answer('Введите корректную сумму', reply_markup=cancel_withdraw)
        return

    await state.set_data({'amount': amount})
    await state.set_state(Withdraw.get_prizm_address)

    admin_settings = await crud_settings.get_by_id(session, id=1)
    amount_to_withdrawal = amount * (1 - admin_settings.withdrawal_commission_percent)

    await message.answer(f'Отправьте адрес кошелька в таком формате:\nPRIZM-****-****-****-****\n\n'
                         f'Комиссия сервиса {admin_settings.commission_percent * 100}%\n'
                         f'Сумма для вывода: {amount:.2f} PZM\n'
                         f'Вы получите с учетом комиссии: {amount_to_withdrawal:.2f} PZM\n',
                         reply_markup=cancel_withdraw)


@router.message(Withdraw.get_prizm_address)
async def check_input_and_withdraw_balance(message: Message, state: FSMContext, user_db: User, session: AsyncSession):
    if not check_wallet_format(message.text):
        await message.answer(f'Отправьте адрес кошелька в таком формате: PRIZM-****-****-****-****',
                             reply_markup=cancel_withdraw)
        return

    amount = await state.get_value('amount')

    prizm_wallet = message.text

    admin_settings = await crud_settings.get_by_id(session, id=1)

    user_db = await crud_user.decrease_balance(session, id=message.from_user.id, summ=float(amount))
    amount_to_withdrawal = amount * (1 - admin_settings.withdrawal_commission_percent)

    main_secret_phrase = settings.PRIZM_WALLET_SECRET_ADDRESS

    prizm_fetcher = PrizmWalletFetcher(settings.PRIZM_API_URL)
    try:
        res = await prizm_fetcher.send_money(prizm_wallet, secret_phrase=main_secret_phrase,
                                       amount_nqt=int(amount_to_withdrawal * 100), deadline=60)
        if res.get('errorCode'):
            raise Exception(res)
        await message.answer('Деньги выведены на указанный адрес', reply_markup=menu_button)
    except :
        user_db = await crud_user.increase_balance(session, id=message.from_user.id, summ=float(amount))
        await message.answer('Возникла ошибка, напишите в поддержку', reply_markup=menu_button)
    await state.clear()
