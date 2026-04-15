from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command 

from app.services.news_service import NewsService

router = Router()


@router.message(Command("news"))
async def get_news(message: Message):
    
    service = NewsService()
    
    news_list = await service.get_latest_news()
    
    if not news_list:
        await message.answer("Сейчас новостей нет.")
        return
    
    text = ""
    
    for n in news_list:
        text += f"<b>{n.title}</b>\n"
        text += f"{n.url}\n\n"
    
    await message.answer(text)
