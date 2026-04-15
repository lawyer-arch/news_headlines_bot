from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command 


router = Router()


@router.message(Command("start"))
async def start(message: Message):

    text = (
        "Бот новостей\n\n"
        "Команды:\n"
        "/news - последние новости\n"
        "/news ria - новости РБК\n"
        "/sources - список источников\n"
        "/subscribe\n"
        "/subscriptions\n"
        "/unsubscribe"
    )
    
    await message.answer(
        text,
        parse_mode="HTML"
    )