from aiogram import Bot
from app.db.session import async_session
from sqlalchemy import select
from app.db.models import Source
from app.services.subscription_service import SubscriptionService


class NotificationService:

    def __init__(self, bot: Bot):
        self.bot = bot
        self.sub_service = SubscriptionService()

    async def send_news(self, news_list):
        print(f"=== NOTIFICATION: received {len(news_list)} news ===")
    
        for news in news_list:
            print(f"News: title={news.title}, source_id={news.source_id}")
        
            # Проверим, какой источник по этому ID
            async with async_session() as session:
                result = await session.execute(
                    select(Source.name).where(Source.id == news.source_id)
                )
                source_name = result.scalar_one_or_none()
                print(f"Source name for ID {news.source_id}: {source_name}")
        
            subscribers = await self.sub_service.get_subscribers(news.source_id)
            print(f"Subscribers for source_id {news.source_id}: {subscribers}")
        
            if not subscribers:
                print(f"No subscribers for source_id {news.source_id}")
                continue
        
            text = f"<b>{news.title}</b>\n{news.url}"
        
            for user_id in subscribers:
                try:
                    await self.bot.send_message(user_id, text)
                    print(f"Sent to {user_id}")
                except Exception as e:
                    print(f"Failed to send to {user_id}: {e}")