from aiogram.types import BotCommand


def get_default_commands() -> list[BotCommand]:
    return [
        BotCommand(command="start", description='Начать'),
    ]
