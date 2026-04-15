from sqlalchemy import select

from app.db.session import async_session
from app.db.models import News


class NewsService:

    async def get_latest_news(self, limit=10):

        async with async_session() as session:

            query = (
                select(News)
                .order_by(News.published_at.desc())
                .limit(limit)
            )

            result = await session.execute(query)

            return result.scalars().all()

    async def save_news(self, news_list):

        async with async_session() as session:

            for item in news_list:
                
                query = select(News).where(News.url == item["url"])
                
                result = await session.execute(query)

                exists = result.scalar()

                if exists:
                    continue
                
                news = News(
                    title=item["title"],
                    url=item["url"],
                    source_id=1
                )

                session.add(news)

            await session.commit()
