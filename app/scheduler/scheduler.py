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
            print("=== UPDATE_NEWS START ===")
            news = await fetch_all_news()
            print(f"Fetched {len(news)} news total")
            
            if not news:
                logging.warning("No news fetched")
                return

            new_news = await news_service.save_news(news)
            print(f"Saved {len(new_news)} new news")
            if new_news:
                sources_in_new = set()
                for n in new_news:
                    sources_in_new.add(n.source_id)
                print(f"Sources in new news: {sources_in_new}")

                print(f"Sending notifications for {len(new_news)} news")
                await notifier.send_news(new_news)
                print("Notifications sent")
            else:
                print("No new news to notify")

        except Exception:
            logging.exception("update_news failed")

    scheduler.add_job(
        update_news,
        "interval",
        minutes=1,
        id="update_news_job",
        replace_existing=True,
        max_instances=1
    )

    scheduler.start()
