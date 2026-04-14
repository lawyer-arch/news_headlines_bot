import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from app.bot.handlers import start, news
from app.scheduler.scheduler import start_scheduler
from app.config import settings


async def main():
    async with Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    ) as bot:
        
        dp = Dispatcher()
    
        dp.include_router(start.router)
        dp.include_router(news.router)

        start_scheduler()

        try:
            await dp.start_polling(bot)
        except asyncio.CancelledError:
            print("Polling cancelled, exiting...")


if __name__ == "__main__":

    asyncio.run(main())