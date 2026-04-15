from sqlalchemy import select

from app.db.session import async_session
from app.db.models import News, Source


class NewsService:

    async def get_latest_news(self, limit=10, source_name=None):

        async with async_session() as session:

            query = (
                select(News)
                .order_by(News.published_at.desc())
                .limit(limit)
            )

            if source_name and source_name != "all":

                query = (
                    query.join(Source)
                    .where(Source.name == source_name)
                )

            query = query.limit(limit)

            result = await session.execute(query)

            return result.scalars().all()

    async def save_news(self, news_list):

        async with async_session() as session:

            new_news = []

            for item in news_list:
 
                query = select(News).where(News.url == item["url"])
                result = await session.execute(query)

                exists = result.scalar_one_or_none()

                if exists:
                    continue

                source_query = select(Source).where(
                    Source.name == item["source"]
                    )
                source_result = await session.execute(source_query)
                source = source_result.scalar_one_or_none()

                if not source:
                    source = Source(
                        name=item["source"],
                        url=item.get("source_url", "")
                    )
                    session.add(source)
                    await session.flush()

                news = News(
                    title=item["title"],
                    url=item["url"],
                    source_id=source.id,
                    published_at=item.get("published_at")
                )

                session.add(news)

                new_news.append(news)

            await session.commit()

            return new_news
