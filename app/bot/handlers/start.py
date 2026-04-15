from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command 


router = Router()


@router.message(Command("start"))
async def start(message: Message):

    await message.answer(
        "Бот новостей\n\n"
        "Команды:\n"
        "/news - последние новости\n"
        "/subscribe <source>\n"
        "/subscriptions\n"
        "/unsubscribe <source>"
    )