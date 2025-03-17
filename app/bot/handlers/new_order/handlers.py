from logging import getLogger

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import ManagedTextInput

from app.bot.handlers.common import start_cmd
from app.bot.handlers.new_order.state import NewOrderState
from app.bot.ui import get_menu_kb
from app.bot.ui.texts import get_start_text
from app.core.config import settings
from app.core.dao import crud_order_request, crud_settings
from app.core.dao.crud_wallet import crud_wallet
from app.core.dto import WalletCreate, OrderRequestCreate
from app.core.models import OrderRequest, User
from app.utils.coinmarketcap import get_currency_rate, rate_difference
from app.utils.text_check import check_phone_format, check_card_format, check_wallet_format

logger = getLogger(__name__)


async def cancel_logic(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await callback.message.answer("Вы отменили создание ордера")
    await dialog_manager.done()
    await start_cmd(callback.message, callback.bot, dialog_manager.middleware_data['state'],
                    dialog_manager.middleware_data['user_db'], dialog_manager)


async def on_back(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    if dialog_manager.start_data['mode'] == 'sell':
        await dialog_manager.switch_to(state=NewOrderState.card_method_details, show_mode=ShowMode.DELETE_AND_SEND)
        return
    else:
        await dialog_manager.switch_to(state=NewOrderState.rate, show_mode=ShowMode.DELETE_AND_SEND)


async def on_from_value_selected(message: Message, text_widget: ManagedTextInput, dialog_manager: DialogManager, data):
    dialog_manager.dialog_data['from_value'] = text_widget.get_value()
    await dialog_manager.next(show_mode=ShowMode.DELETE_AND_SEND)


async def on_to_value_selected(message: Message, text_widget: ManagedTextInput, dialog_manager: DialogManager, data):
    dialog_manager.dialog_data['to_value'] = text_widget.get_value()

    await dialog_manager.next(show_mode=ShowMode.DELETE_AND_SEND)


async def on_rate_selected(message: Message, text_widget: ManagedTextInput, dialog_manager: DialogManager, data):
    dialog_manager.dialog_data['rate'] = user_rate = text_widget.get_value()
    rate = await get_currency_rate("PZM", "RUB", settings.COINMARKETCAP_API_KEY)
    async with dialog_manager.middleware_data['session'] as session:
        admin_settings = await crud_settings.get_by_id(session, id=1)
        prizm_rate_diff_percent = admin_settings.prizm_rate_diff * 100

    if rate_difference(rate, user_rate, prizm_rate_diff_percent):
        await message.answer(parse_mode='html',
                             text=f'Указанный курс отличается от биржевого более чем на <b>{prizm_rate_diff_percent}</b>%.\nТекущий курс: <b>{str(rate)[:7]}</b>')
        return

    if dialog_manager.start_data['mode'] == 'sell':
        await dialog_manager.switch_to(state=NewOrderState.card_method_details, show_mode=ShowMode.DELETE_AND_SEND)
    else:
        await dialog_manager.switch_to(state=NewOrderState.sell_card_info, show_mode=ShowMode.DELETE_AND_SEND)


async def on_card_method_selected(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """Обработчик выбора количества гостей."""
    dialog_manager.dialog_data['card_method'] = callback.data
    await dialog_manager.switch_to(state=NewOrderState.sell_card_info, show_mode=ShowMode.DELETE_AND_SEND)


async def on_sell_card_info_selected(message: Message, text_widget: ManagedTextInput, dialog_manager: DialogManager,
                                     data):
    sell_card_info = text_widget.get_value()

    if dialog_manager.start_data['mode'] == 'sell':
        if dialog_manager.dialog_data['card_method'] == "sbp":
            if not check_phone_format(sell_card_info):
                return
        elif dialog_manager.dialog_data['card_method'] == "card":
            if not check_card_format(sell_card_info):
                return

    else:
        if not check_wallet_format(sell_card_info):
            return

    value_rate = dialog_manager.dialog_data['rate']
    min_limit_rub = dialog_manager.dialog_data['from_value'] * value_rate
    max_limit_rub = dialog_manager.dialog_data['to_value'] * value_rate
    user_db = dialog_manager.middleware_data['user_db']
    async with dialog_manager.middleware_data['session'] as session:
        admin_settings = await crud_settings.get_by_id(session, id=1)
        if dialog_manager.start_data['mode'] == 'sell':
            from_currency = "PRIZM"
            to_currency = "RUB"
            wallet_currency = 'RUB'
            order_request_status = OrderRequest.WAIT_PRIZM
        else:
            from_currency = "RUB"
            to_currency = "PRIZM"
            wallet_currency = 'PRIZM'
            order_request_status = OrderRequest.IN_PROGRESS
        wallet = await crud_wallet.get_by_user_id_currency(session, currency=wallet_currency,
                                                           user_id=dialog_manager.middleware_data['user_db'].id)
        if not wallet:
            wallet = WalletCreate(user_id=message.from_user.id, currency=wallet_currency, value=sell_card_info)
            await crud_wallet.create(session, obj_in=wallet)
        elif wallet.value != sell_card_info:
            await crud_wallet.update(session, db_obj=wallet, obj_in={"value": sell_card_info})

        order_request = OrderRequestCreate(
            user_id=message.from_user.id,
            from_currency=from_currency,
            to_currency=to_currency,
            min_limit=dialog_manager.dialog_data['from_value'],
            max_limit=dialog_manager.dialog_data['to_value'],
            min_limit_rub=min_limit_rub,
            max_limit_rub=max_limit_rub,
            rate=dialog_manager.dialog_data['rate'],
            status=order_request_status
        )
        order_request = await crud_order_request.create(session, obj_in=order_request)
    if dialog_manager.start_data['mode'] == 'sell':
        value_with_commission = dialog_manager.dialog_data['to_value'] + dialog_manager.dialog_data[
            'to_value'] * admin_settings.commission_percent
        text = (
            f"Переведите {value_with_commission} PZM c коммиссией сервиса {admin_settings.commission_percent * 100}%\nБез комментария платеж потеряется!\n"
            f"На кошелек сервиса:\n<b>{settings.PRIZM_WALLET_ADDRESS}</b>\n"
            f"Комментарий платежа:\n<b>request:{order_request.user_id}:{order_request.id}</b>\n\n"
            f"⏳Перевод надо совершить в течении {admin_settings.pay_wait_time} минут.")
        await message.bot.send_message(message.from_user.id, text=text, parse_mode='html')
        await message.bot.send_message(message.from_user.id, settings.PRIZM_WALLET_ADDRESS)
        await message.bot.send_message(message.from_user.id, f"request:{order_request.user_id}:{order_request.id}")
    else:
        text = (f"Ваш ордер №{order_request.id} на покупку PRIZM создан и размещен в боте.\n"
                f"Ордер: №{order_request.id}\nКурс 1pzm - {order_request.rate}руб\nЛимит: {order_request.min_limit_rub} - {order_request.max_limit_rub}руб\nЧисло сделок:{user_db.order_count} Число отказов: {user_db.cancel_order_count}\n\n") + get_start_text(
            user_db.balance, user_db.order_count,
            user_db.cancel_order_count)

        await message.bot.send_message(message.from_user.id, text=text,
                                       reply_markup=get_menu_kb(is_admin=user_db.role == User.ADMIN_ROLE))
    await dialog_manager.done(show_mode=ShowMode.DELETE_AND_SEND)
