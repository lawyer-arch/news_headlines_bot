from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.parsers.kommersant import fetch_news


scheduler = AsyncIOScheduler()


async def update_news():

    news = await fetch_news()

    print(news)


def start_scheduler():

    scheduler.add_job(update_news, "interval", minutes=5)

    scheduler.start()