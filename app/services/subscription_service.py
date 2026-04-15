from sqlalchemy import select, delete

from app.db.session import async_session
from app.db.models import Subscription, User, Source


class SubscriptionService:

    async def subscribe(self, telegram_id: int, source_name: str):

        async with async_session() as session:

            # получаем пользователя
            user_query = select(User).where(User.telegram_id == telegram_id)
            user_result = await session.execute(user_query)
            user = user_result.scalar_one_or_none()

            if not user:
                user = User(telegram_id=telegram_id)
                session.add(user)
                await session.flush()

            # получаем источник
            source_query = select(Source).where(Source.name == source_name)
            source_result = await session.execute(source_query)
            source = source_result.scalar_one_or_none()

            if not source:
                return False, "Источник не найден"

            # проверяем подписку
            sub_query = select(Subscription).where(
                Subscription.user_id == user.id,
                Subscription.source_id == source.id
            )

            sub_result = await session.execute(sub_query)
            exists = sub_result.scalar_one_or_none()

            if exists:
                return False, "Вы уже подписаны"

            sub = Subscription(
                user_id=user.id,
                source_id=source.id
            )

            session.add(sub)
            await session.commit()

            return True, f"Подписка на {source_name} добавлена"


    async def get_user_subscriptions(self, telegram_id: int):

        async with async_session() as session:

            query = (
                select(Source.name)
                .join(Subscription, Subscription.source_id == Source.id)
                .join(User, User.id == Subscription.user_id)
                .where(User.telegram_id == telegram_id)
            )

            result = await session.execute(query)

            return result.scalars().all()


    async def unsubscribe(self, telegram_id: int, source_name: str):

        async with async_session() as session:

            query = (
                select(Subscription)
                .join(User)
                .join(Source)
                .where(
                    User.telegram_id == telegram_id,
                    Source.name == source_name
                )
            )

            result = await session.execute(query)
            sub = result.scalar_one_or_none()

            if not sub:
                return False, "Подписка не найдена"

            await session.delete(sub)
            await session.commit()

            return True, f"Подписка на {source_name} удалена"
