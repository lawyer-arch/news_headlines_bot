from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.db.models import News


class NewsService:

    async def get_latest_news(self, limit=10):

        async with AsyncSessionLocal() as session:

            query = (
                select(News)
                .order_by(News.published_at.desc())
                .limit(limit)
            )

            result = await session.execute(query)

            return result.scalars().all()