FROM python:3.12-alpine

RUN apk add --no-cache build-base libffi-dev openssl-dev curl git bash

RUN pip install --no-cache-dir poetry==2.1.1

WORKDIR /app

COPY pyproject.toml poetry.lock README.md ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-root

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]