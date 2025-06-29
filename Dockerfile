FROM python:3.12-slim

RUN pip install poetry

WORKDIR /code

COPY README.md .

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-interaction --no-root

COPY . .

RUN mkdir -p /code/media/restaurant/images

RUN mkdir -p /code/media/restaurant/workers/images

EXPOSE 8000

CMD ["sh", "-c", "poetry run python manage.py migrate && poetry run python manage.py runserver 0.0.0.0:8000"]