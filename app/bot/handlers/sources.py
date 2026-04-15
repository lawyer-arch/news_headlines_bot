from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from app.db.session import async_session
from app.db.models import Source
from sqlalchemy import select

router = Router()


@router.message(Command("sources"))
async def sources(message: Message):

    async with async_session() as session:

        result = await session.execute(select(Source))

        sources = result.scalars().all()

    if not sources:
        await message.answer("Источники пока не добавлены")
        return

    text = "Доступные источники:\n\n"

    for s in sources:
        text += f"• {s.name}\n"

    await message.answer(text)