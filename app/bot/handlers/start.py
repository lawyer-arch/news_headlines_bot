from aiogram import Router
from aiogram.types import Message


router = Router()


@router.message(commands=["start"])
async def start(message: Message):

    await message.answer(
        "Бот новостей.\n"
        "Команды:\n"
        "/news - последние новости"
    )