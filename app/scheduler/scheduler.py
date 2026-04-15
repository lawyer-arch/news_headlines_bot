from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.services.news_service import NewsService
from app.parsers.kommersant import fetch_news


scheduler = AsyncIOScheduler()


async def update_news():

    service = NewsService()

    news_list = await fetch_news()

    await service.save_news(news_list)


def start_scheduler():
    scheduler.add_job(update_news, "interval", minutes=20)
    scheduler.start()
