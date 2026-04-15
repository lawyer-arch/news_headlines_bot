from sqlalchemy import select

from app.db.session import async_session
from app.db.models import News, Source


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
                # Проверяем, есть ли уже такая новость
                query = select(News).where(News.url == item["url"])
                result = await session.execute(query)
                exists = result.scalar()

                if exists:
                    continue
                
                # Ищем источник по имени
                source_query = select(Source).where(Source.name == item["source"])
                source_result = await session.execute(source_query)
                source = source_result.scalar_one_or_none()
                
                if not source:
                    # Если источника нет, создаем
                    source = Source(
                        name=item["source"],
                        url=item.get("source_url", f"https://{item['source']}.com")
                    )
                    session.add(source)
                    await session.flush()
                
                # Создаем новость с правильным source_id
                news = News(
                    title=item["title"],
                    url=item["url"],
                    source_id=source.id,
                    published_at=item.get("published_at")
                )

                session.add(news)

            await session.commit()
