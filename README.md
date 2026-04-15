Описание проекта

Архитектура

Схема БД
Для PostgreSQL создаем БД "news_headline_db"

Установите Alembic (если его еще нет):
pip install alembic

Инициализируйте Alembic в вашем проекте:
alembic init alembic

Создаеь миграцию:
alembic revision --autogenerate -m "Init: create tables for users, sources, news and subscriptions"

Примените миграцию к базе данных:
alembic upgrade head

Как запустить
Устанавливаем виртуальное окружение .venv.
Разворачиваем 

docker compose up --build