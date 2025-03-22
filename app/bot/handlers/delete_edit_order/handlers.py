from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button
from sqlalchemy.testing.suite.test_reflection import users

from app.bot.handlers.delete_edit_order.state import DeleteEditOrder
from app.bot.ui import get_menu_kb
from app.bot.ui.texts import get_start_text
from app.core.config import settings
from app.core.dao import crud_order_request, crud_settings, crud_user
from app.core.models import User, OrderRequest
from app.prizm_check_scheduler.prizm_fetcher import PrizmWalletFetcher
from app.utils.coinmarketcap import get_currency_rate, rate_difference
from app.utils.text_check import check_wallet_format

async def on_back_edit_points_window(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):

    await dialog_manager.switch_to(state=DeleteEditOrder.update_menu, show_mode=ShowMode.DELETE_AND_SEND)


async def start(callback, button, dialog_manager: DialogManager):
    user_db = dialog_manager.middleware_data['user_db']
    await dialog_manager.done()
    await callback.bot.send_message(
        user_db.id, get_start_text(user_db.balance, user_db.order_count, user_db.cancel_order_count),
        reply_markup=get_menu_kb(is_admin=user_db.role == User.ADMIN_ROLE)
    )


async def order_menu(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, data):
    dialog_manager.dialog_data['order_id'] = data
    await dialog_manager.switch_to(DeleteEditOrder.order_menu)


async def continue_or_stop_order(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    session = dialog_manager.middleware_data['session']
    if callback.data == 'continue_order':
        order = await crud_order_request.get_by_id(session, id=int(dialog_manager.dialog_data['order_id']))
        await crud_order_request.update(session, db_obj=order, obj_in={'status': OrderRequest.IN_PROGRESS})
        await dialog_manager.switch_to(state=DeleteEditOrder.order_menu, show_mode=ShowMode.DELETE_AND_SEND)
    else:
        order = await crud_order_request.get_by_id(session, id=int(dialog_manager.dialog_data['order_id']))
        await crud_order_request.update(session, db_obj=order, obj_in={'status': OrderRequest.STOPPED})
        await dialog_manager.switch_to(state=DeleteEditOrder.order_menu, show_mode=ShowMode.DELETE_AND_SEND)


async def delete_order(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    session = dialog_manager.middleware_data['session']
    order = await crud_order_request.get_by_id(session, id=int(dialog_manager.dialog_data['order_id']))

    await crud_user.increanse_balance(session, id=callback.from_user.id, summ=order.max_limit)

    await crud_order_request.update(session, db_obj=order, obj_in={'status': OrderRequest.CLOSED})
    await callback.message.answer('Ордер удален')
    await start(callback, button, dialog_manager)


async def error_handler(
        message: Message,
        widget: ManagedTextInput,
        manager: DialogManager,
        error: ValueError
):
    await message.answer("Введите корректную сумму")


async def update_min_sum(message: Message,
                         widget: ManagedTextInput,
                         dialog_manager: DialogManager,
                         data):
    session = dialog_manager.middleware_data['session']
    order = await crud_order_request.get_by_id(session, id=int(dialog_manager.dialog_data['order_id']))
    if float(data) < order.max_limit:
        await crud_order_request.update(session, db_obj=order, obj_in={'min_limit': float(data)})
        await message.answer('Обновлено')
        await start(message, widget, dialog_manager)
        return
    await message.answer('Минимальная сумма должна быть меньше максимальной')


async def update_max_sum(message: Message, widget: ManagedTextInput,
                         dialog_manager: DialogManager, data):
    data = float(data)
    session = dialog_manager.middleware_data['session']
    order_request = await crud_order_request.get_by_id(session, id=int(dialog_manager.dialog_data['order_id']))
    if data < order_request.max_limit or order_request.from_currency == 'RUB':
        await crud_order_request.update(session, db_obj=order_request, obj_in={'max_limit': data})
        await message.answer('Обновлено')
        await dialog_manager.switch_to(state=DeleteEditOrder.update_menu, show_mode=ShowMode.DELETE_AND_SEND)
        return

    admin_settings = await crud_settings.get_by_id(session, id=1)
    value_with_commission = data + data * admin_settings.commission_percent - order_request.max_limit
    text = (
        f"Переведите {value_with_commission} PZM c коммиссией сервиса {admin_settings.commission_percent * 100}%"
        f"\nБез комментария платеж потеряется!\n"
        f"На кошелек сервиса:\n<b>{settings.PRIZM_WALLET_ADDRESS}</b>\n"
        f"Комментарий платежа:\n<b>request:{order_request.user_id}:{order_request.id}</b>\n\n"
        f"⏳Перевод надо совершить в течении {admin_settings.pay_wait_time} минут.")
    await message.answer(text=text, parse_mode='html')
    await message.answer(settings.PRIZM_WALLET_ADDRESS)
    await message.answer(f"request:{order_request.user_id}:{order_request.id}")

    await crud_order_request.update(session, db_obj=order_request, obj_in={'status': OrderRequest.WAIT_PRIZM})
    await dialog_manager.done()


async def update_cource(message: Message,
                        widget: ManagedTextInput,
                        dialog_manager: DialogManager,
                        data):
    user_rate = float(data)
    session = dialog_manager.middleware_data['session']
    rate = await get_currency_rate("PZM", "RUB", settings.COINMARKETCAP_API_KEY)
    admin_settings = await crud_settings.get_by_id(session, id=1)
    prizm_rate_diff_percent = admin_settings.prizm_rate_diff * 100

    if rate_difference(rate, user_rate, prizm_rate_diff_percent):
        await message.answer(parse_mode='html',
                             text=f'Указанный курс отличается от биржевого более чем на <b>{prizm_rate_diff_percent}</b>'
                                  f'%.\nТекущий курс: <b>{str(rate)[:7]}</b>')
        return

    order = await crud_order_request.get_by_id(session, id=int(dialog_manager.dialog_data['order_id']))
    await crud_order_request.update(session, db_obj=order, obj_in={'rate': data})
    await message.answer('Обновлено')
    await dialog_manager.switch_to(state=DeleteEditOrder.update_menu, show_mode=ShowMode.DELETE_AND_SEND)
