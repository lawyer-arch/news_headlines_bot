from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command 

from app.services.news_service import NewsService

router = Router()


@router.message(Command("news"))
async def get_news(message: Message):

    service = NewsService()

    news_list = await service.get_latest_news()

    text = ""

    for n in news_list:

        text += f"{n.title}\n{n.url}\n\n"
    
    if text != "":
        await message.answer(text)
    await message.answer("Пока новостей нет")