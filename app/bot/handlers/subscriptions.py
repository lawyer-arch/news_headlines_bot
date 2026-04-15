from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from app.services.subscription_service import SubscriptionService

router = Router()

service = SubscriptionService()


@router.message(Command("subscribe"))
async def subscribe(message: Message):

    args = message.text.split()

    if len(args) < 2:
        await message.answer(
            "Использование:\n"
            "/subscribe <источник>\n\n"
            "Пример:\n"
            "/subscribe rbk"
        )
        return

    source = args[1].lower()

    ok, text = await service.subscribe(
        message.from_user.id,
        source
    )

    await message.answer(text)


@router.message(Command("subscriptions"))
async def subscriptions(message: Message):

    subs = await service.get_user_subscriptions(
        message.from_user.id
    )

    if not subs:
        await message.answer("У вас нет подписок")
        return

    text = "Ваши подписки:\n\n"

    for s in subs:
        text += f"• {s}\n"

    await message.answer(text)


@router.message(Command("unsubscribe"))
async def unsubscribe(message: Message):

    args = message.text.split()

    if len(args) < 2:
        await message.answer(
            "Использование:\n"
            "/unsubscribe <источник>"
        )
        return

    source = args[1].lower()

    ok, text = await service.unsubscribe(
        message.from_user.id,
        source
    )

    await message.answer(text)