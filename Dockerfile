FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install -r pyproject.toml

CMD ["python", "-m", "app.main"]