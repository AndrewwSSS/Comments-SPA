FROM python:3.10

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

RUN apt-get update && apt-get install -y dos2unix && rm -rf /var/lib/apt/lists/*

COPY . .

COPY entrypoint.sh ws-entrypoint.sh ./

RUN dos2unix entrypoint.sh ws-entrypoint.sh

RUN chmod +x entrypoint.sh ws-entrypoint.sh

CMD ["sh", "entrypoint.sh"]
