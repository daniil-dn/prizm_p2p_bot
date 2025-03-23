from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.handlers.admin.state import AdminSettingsState, GetHistoryMessage
from app.bot.middlewares.check_admin import check_admin
from app.bot.ui import get_menu_kb
from app.core.dao.crud_message import crud_message
from app.core.models import User

router = Router()


@router.callback_query(F.data.startswith('admin_panel_command'))
@check_admin
async def admin_menu_cb(cb: CallbackQuery, bot: Bot, state: FSMContext, user_db: User,
                        dialog_manager: DialogManager) -> None:
    admin_command = cb.data.split('_')[-1]
    if admin_command == 'new-commission':
        await dialog_manager.start(state=AdminSettingsState.new_value_commission, mode=StartMode.RESET_STACK)
    elif admin_command == 'new-order-wait-time':
        await dialog_manager.start(state=AdminSettingsState.new_order_time, mode=StartMode.RESET_STACK)
    elif admin_command == 'new-pay-order-wait-time':
        await dialog_manager.start(state=AdminSettingsState.new_pay_order_time, mode=StartMode.RESET_STACK)
    elif admin_command == 'new-rate-diff':
        await dialog_manager.start(state=AdminSettingsState.new_prizm_rate_diff_value, mode=StartMode.RESET_STACK)

    elif admin_command == 'add-admin-by-username':
        await dialog_manager.start(state=AdminSettingsState.add_admin_by_username, mode=StartMode.RESET_STACK)

    elif admin_command == 'remove-admin-by-username':
        await dialog_manager.start(state=AdminSettingsState.remove_admin_by_username, mode=StartMode.RESET_STACK)
    elif admin_command == 'message-history':
        await state.set_state(GetHistoryMessage.wait_for_id)
        await cb.message.answer('Введите ID сделки')


@router.message(GetHistoryMessage.wait_for_id)
async def get_history(message: Message, state: FSMContext, session: AsyncSession, user_db: User):
    if not message.text.isdigit():
        await message.answer('Айди должно быть числом. попробуйте снова')
        return
    await state.clear()
    history = await crud_message.get_all_by_order_id(session, int(message.text))
    text = ''
    files = []
    for archive_message in history:
        if archive_message.text:
            text += (f'От пользователя {archive_message.from_user.username} ({archive_message.from_user.id}) в '
                     f'{archive_message.created_at}:\n{archive_message.text}\n\n')
        if archive_message.photo:
            files.append((archive_message.photo, 'photo'))
        elif archive_message.document:
            files.append((archive_message.document, 'document'))

    if text == '':
        text = 'Отсутствует переписка'

    await message.answer(text)
    for file, type_file in files:
        try:
            if type_file == 'photo':
                await message.answer_photo(file)
            else:
                await message.answer_document(file)
        except:
            pass
    await message.answer('Выберите пункт меню', reply_markup=get_menu_kb(is_admin=user_db.role == User.ADMIN_ROLE))