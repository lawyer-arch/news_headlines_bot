from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging

from app.parsers.manager import fetch_all_news
from app.services.news_service import NewsService

scheduler = AsyncIOScheduler()
service = NewsService()


async def update_news():
    try:
        news = await fetch_all_news()

        if not news:
            logging.warning("No news fetched")
            return

        await service.save_news(news)

    except Exception as e:
        logging.exception(f"update_news failed: {e}")


def start_scheduler():
    scheduler.add_job(
        update_news,
        "interval",
        minutes=5,
        id="update_news_job",
        replace_existing=True,
        coalesce=True,
        max_instances=1,
        misfire_grace_time=60,
    )

    scheduler.start()
