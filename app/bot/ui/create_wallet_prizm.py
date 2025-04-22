from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

activate_wallet_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='👛 Создать кошелек', url="https://wallet.prizm.vip/")],
    [InlineKeyboardButton(text='🔓 Активировать кошелек', callback_data='activate_wallet_prizm')],
    [InlineKeyboardButton(text='🏠 Главное меню', callback_data='start_bot')]
], resize_keyboard=True)

back_to_create_wallet = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='❌ Отмена', callback_data='create_wallet_prizm')]
])
