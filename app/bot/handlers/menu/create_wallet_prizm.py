from logging import getLogger

from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.handlers.menu.states import ActivatePrizmWallet
from app.bot.ui.create_wallet_prizm import activate_wallet_kb, back_to_create_wallet
from app.bot.ui.menu import menu_button
from app.core.config import settings
from app.core.dao import crud_user
from app.core.dto import UserUpdate
from app.core.models import User
from app.prizm_check_scheduler.prizm_fetcher import PrizmWalletFetcher
from app.utils.text_check import check_wallet_format

router = Router()

logger = getLogger(__name__)

@router.callback_query(F.data.startswith('create_wallet_prizm'))
async def instruction_msg(cb: CallbackQuery, bot: Bot, state: FSMContext, user_db: User) -> None:
    await state.clear()
    await cb.message.edit_reply_markup(reply_markup=None)

    reply_kb = activate_wallet_kb if not user_db.is_wallet_activated else menu_button

    await bot.send_message(
        cb.from_user.id,
        f"""
Для создания кошелька нажмите на кнопку ниже. 

⚠️ После создания парольной фразы обязательно сохраните ее в надежном месте перед входом в кошелек. Без нее доступ к средствам будет утерян. 

Также для использования кошелька его необходимо активировать. Для этого Вам будет выслано на  созданный Вами кошелек 0.5 PZM. 
Активация проводится только один раз.
""", parse_mode="html", reply_markup=reply_kb)

@router.callback_query(F.data.startswith('activate_wallet_prizm'))
async def activate_wallet_prizm(cb: CallbackQuery, bot: Bot, state: FSMContext, user_db: User) -> None:
    await state.clear()
    await cb.message.edit_reply_markup(reply_markup=None)

    await bot.send_message(
        cb.from_user.id,
        f"""Отправьте адрес кошелька, который нужно активировать в таком формате: PRIZM-****-****-****-****.""", parse_mode="html", reply_markup=back_to_create_wallet)
    await state.set_state(ActivatePrizmWallet.get_wallet)

@router.message(ActivatePrizmWallet.get_wallet)
async def activate_wallet_prizm(message: Message, bot: Bot, state: FSMContext, user_db: User, session: AsyncSession) -> None:
    if not check_wallet_format(message.text):
        await message.answer(f'Отправьте адрес кошелька в таком формате: PRIZM-****-****-****-****',
                             reply_markup=back_to_create_wallet)
        return

    prizm_wallet = message.text

    logger.info(
        f"Активация кошелька {prizm_wallet} для юзера: {message.from_user.id}")

    main_secret_phrase = settings.PRIZM_WALLET_SECRET_ADDRESS

    prizm_fetcher = await PrizmWalletFetcher().init_with_active_node(session)
    try:
        await prizm_fetcher.send_money(prizm_wallet, secret_phrase=main_secret_phrase,
                                       amount_nqt=50, deadline=60)
        await message.answer(f'Кошелек {prizm_wallet} активирован!', reply_markup=menu_button)
        logger.info(f'Кошелек активирован {prizm_wallet} для юзера: {message.from_user.id}')
        await crud_user.update(session, db_obj=user_db, obj_in=UserUpdate(is_wallet_activated=True))
    except Exception as err:
        logger.error(f"Send pzm to {prizm_wallet} Error: {err}")
        await message.answer('Возникла ошибка, напишите в поддержку', reply_markup=menu_button)
    await state.clear()