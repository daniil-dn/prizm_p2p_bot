from aiogram_dialog import DialogManager

from app.core.dao import crud_chat_channel


async def chats_getter(dialog_manager: DialogManager, **kwargs):
    chats = await crud_chat_channel.get_by_user_id(dialog_manager.middleware_data['session'],
                                                   user_id=dialog_manager.middleware_data['event_from_user'].id)

    text = 'Ваши чаты:\n'

    for chat in chats:
        text += f'{chat.username or chat.name or chat.id}\n'

    return {'there': bool(chats),
            'text': text,
            'chats': chats}


async def chat_getter(dialog_manager: DialogManager, **kwargs):
    chat = await crud_chat_channel.get_by_id(dialog_manager.middleware_data['session'],
                                                   id=int(dialog_manager.dialog_data['selected_chat']))

    text=(f'ID чата: {chat.id}\n' +
          (f'Username: @{chat.username}\n' if chat.username else '') +
          (f'Название: {chat.name}\n' if chat.name else '') +
          f'Кол-во в день: {chat.count_in_day}\n'
          f'Время между постами: {chat.interval}\n'
          f'Интервал в течение дня: {chat.interval_in_day}.\n'
          f'{'На паузе ⏸️' if chat.is_stopped else 'Активен ▶️'}\n\n'
          f'Выберите, что вы хотите изменить:')


    return {'text': text,
            'chat': chat}