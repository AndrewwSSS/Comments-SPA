FROM python:3.10

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . /app/

CMD ["python", "backend/manage.py", "runserver", "0.0.0.0:8000"]
