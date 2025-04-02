from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.handlers.menu.states import Withdraw
from app.bot.ui import get_menu_kb
from app.bot.ui.texts import get_start_text
from app.bot.ui.withdraw import cancel_withdraw
from app.core.config import settings
from app.core.dao import crud_user, crud_settings
from app.core.models import User
from app.prizm_check_scheduler.prizm_fetcher import PrizmWalletFetcher
from app.utils.text_check import check_wallet_format

router = Router()


@router.callback_query(F.data == 'withdraw_balance')
async def ask_how_many(callback: CallbackQuery, state: FSMContext, user_db: User):
    await state.set_state(Withdraw.get_count_money)
    await callback.message.answer(f'Введите сумму для вывода. Ваш текущий баланс: {user_db.balance}',
                                  reply_markup=cancel_withdraw)


@router.message(Withdraw.get_count_money)
async def check_input_and_ask_address(message: Message, state: FSMContext, user_db: User):
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

    await message.answer('Отправьте адрес кошелька в таком формате: PRIZM-****-****-****-****',
                         reply_markup=cancel_withdraw)


@router.message(Withdraw.get_prizm_address)
async def check_input_and_withdraw_balance(message: Message, state: FSMContext, user_db: User, session: AsyncSession):
    if not check_wallet_format(message.text):
        await message.answer('Отправьте адрес кошелька в таком формате: PRIZM-****-****-****-****',
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
        await prizm_fetcher.send_money(prizm_wallet, secret_phrase=main_secret_phrase,
                                       amount_nqt=int(amount_to_withdrawal * 100), deadline=60)
        await message.answer('Деньги выведены на указанный адрес')
        await message.answer(get_start_text(user_db.balance, user_db.order_count, user_db.cancel_order_count),
            reply_markup=get_menu_kb(is_admin=user_db.role in User.ALL_ADMINS)
        )
    except:
        await message.answer('Возникла ошибка, напишите в поддержку')
    await state.clear()