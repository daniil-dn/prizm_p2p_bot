from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.bot.ui.create_wallet_prizm import menu_button
from app.core.models import User

router = Router()


@router.callback_query(F.data.startswith('create_wallet_prizm'))
async def instruction_msg(cb: CallbackQuery, bot: Bot, state: FSMContext, user_db: User) -> None:
    await state.clear()

    await bot.send_message(
        cb.from_user.id,
        f"""
Для создания кошелька перейдите по ссылке ниже.

В поле для ввода адреса нажмите на изображение человека. 

Оно сменится на ключ 🗝

После этого введите совершенно любой пароль. 

Буквы, цифры, русские или латинские. Символы и т.д. 

<b>⚠️ ОБЯЗАТЕЛЬНО СОХРАНИТЕ ЭТОТ ПАРОЛЬ ПЕРЕД ВХОДОМ В КОШЕЛЕК. 
БЕЗ НЕГО У ВАС НЕ БУДЕТ ВОЗМОЖНОСТИ РАСПОРЯЖАТЬСЯ СРЕДСТВАМИ.

⚠️ ТОЛЬКО ПОСЛЕ ЭТОГО ЗАХОДИТЕ В НОВЫЙ КОШЕЛЕК!</b>

Ссылка для создания кошелька (можно кнопкой):

https://wallet.prizm.vip/
""", parse_mode="html", reply_markup=menu_button)
