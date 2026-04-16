FROM python:3.12-slim as builder

WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Копируем pyproject.toml
COPY pyproject.toml .

# Устанавливаем зависимости через pip (читает pyproject.toml)
RUN pip install --no-cache-dir .

# Финальный образ
FROM python:3.12-slim

WORKDIR /app

# Копируем установленные зависимости из builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Копируем код приложения
COPY . .

# Создаем директорию для логов
RUN mkdir -p /app/app/logs

CMD ["python", "-m", "app.main"]