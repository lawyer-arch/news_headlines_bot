from aiogram import Router
from aiogram.types import Message

from app.services.news_service import NewsService

router = Router()


@router.message(commands=["news"])
async def get_news(message: Message):

    service = NewsService()

    news_list = await service.get_latest_news()

    text = ""

    for n in news_list:

        text += f"{n.title}\n{n.url}\n\n"

    await message.answer(text)