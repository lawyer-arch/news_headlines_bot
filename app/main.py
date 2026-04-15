import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from app.bot.handlers import start, news
from app.scheduler.scheduler import start_scheduler
from config import settings


dp = Dispatcher()


async def main():

    logging.basicConfig(level=logging.INFO)
    async with Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    ) as bot:

        dp.include_router(start.router)
        dp.include_router(news.router)

        start_scheduler()

        try:
            await dp.start_polling(bot)
        except asyncio.CancelledError:
            print("Polling cancelled, exiting...")


if __name__ == "__main__":

    asyncio.run(main())
