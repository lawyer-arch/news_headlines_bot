from aiogram import Bot

from app.services.subscription_service import SubscriptionService


class NotificationService:

    def __init__(self, bot: Bot):
        self.bot = bot
        self.sub_service = SubscriptionService()


    async def send_news(self, news_list):

        for news in news_list:

            subscribers = await self.sub_service.get_subscribers(
                news.source_id
            )

            if not subscribers:
                continue

            text = f"<b>{news.title}</b>\n{news.url}"

            for user_id in subscribers:

                try:
                    await self.bot.send_message(user_id, text)

                except Exception:
                    pass