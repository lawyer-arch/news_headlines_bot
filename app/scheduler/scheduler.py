from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging

from app.parsers.manager import fetch_all_news
from app.services.news_service import NewsService
from app.services.notification_service import NotificationService


scheduler = AsyncIOScheduler()


def start_scheduler(bot):

    news_service = NewsService()
    notifier = NotificationService(bot)

    async def update_news():

        try:

            news = await fetch_all_news()

            if not news:
                logging.warning("No news fetched")
                return

            new_news = await news_service.save_news(news)

            if new_news:
                await notifier.send_news(new_news)

        except Exception:
            logging.exception("update_news failed")

    scheduler.add_job(
        update_news,
        "interval",
        minutes=10,
        id="update_news_job",
        replace_existing=True,
        max_instances=1
    )

    scheduler.start()
