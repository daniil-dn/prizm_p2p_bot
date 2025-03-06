from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command, Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router = Router()


@router.callback_query(F.data.startswith('rules'))
async def rules_msg(message: Message, bot: Bot, state: FSMContext) -> None:
    await state.clear()
    await bot.send_message(
        # todo
        message.from_user.id,
        """Правила сервиса

1. При разовой сделке по покупке или продаже prizm выбирайте в меню "купить Prizm" или "продать Prizm"
2. В случае, если вы покупаете и продаете prizm на постоянной основе, то для удобства воспользуйтесь  разделом "разместить ордер"
3. Будьте предельно внимательны заполняя все необходимые реквизиты и данные. Ошибки могут привести к потере средств. Ответственность за это несете только вы.
4. Просим вас учесть, что администрация сервиса не поддерживает отмывание средств полученных незаконным путем и сотрудничает в этом отношении с правоохранительными органами.
5. При любых затруднениях обращайтесь в службу поддержки, мы постараемся решить Ваш вопрос. 
6. Мы рады получить от Вас любую обратную связь, просьбы и замечания по работе сервиса Вы можете отправить в разделе \"Поддержка\""""
    )
