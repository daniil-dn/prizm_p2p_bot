from logging import getLogger

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import ManagedTextInput

from app.bot.handlers.common import start_cmd
from app.bot.handlers.new_order.state import NewOrderState
from app.bot.ui import get_menu_kb
from app.bot.ui.texts import get_start_text
from app.bot.utils.create_new_order import create_order_and_wallet, send_notification
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
    session = dialog_manager.middleware_data['session']
    admin_settings = await crud_settings.get_by_id(session, id=1)
    prizm_rate_diff_percent = admin_settings.prizm_rate_diff * 100

    if rate_difference(rate, user_rate, prizm_rate_diff_percent):
        await message.answer(parse_mode='html',
                             text=f'Указанный курс отличается от биржевого более чем на <b>{prizm_rate_diff_percent}</b>'
                                  f'%.\nТекущий курс: <b>{str(rate)[:7]}</b>')
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
    order_request, admin_settings = await create_order_and_wallet(dialog_manager=dialog_manager,
                                                                  user_id=message.from_user.id,
                                                                  sell_card_info=sell_card_info)
    await send_notification(dialog_manager=dialog_manager, admin_settings=admin_settings,
                            order_request=order_request, message=message)
    await dialog_manager.done(show_mode=ShowMode.DELETE_AND_SEND)
