import logging
from sqlalchemy.ext.asyncio import create_async_engine

from config import settings
from app.db.models import Base

logger = logging.getLogger(__name__)


async def init_db():
    """Создаёт таблицы, если их нет"""
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    
    async with engine.begin() as conn:
        # Создаём таблицы на основе моделей SQLAlchemy
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Таблицы созданы (или уже существуют)")
    
    await engine.dispose()
