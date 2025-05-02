# Test Task: Django Uptrader

## Описание

Django-приложение, которое реализует древовидное меню с поддержкой вложенных пунктов.  
Меню отображается на веб-странице с выделением активного пункта в зависимости от текущего URL.

Технологии:
- Django 5.2
- SQLite (по умолчанию)
- Docker + Docker Compose (опционально)
- Poetry

## Установка

### Требования

- Python 3.12+
- Poetry
- Docker (опционально)

### Локальный запуск

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/KiselevDV/test_task_django_uptrader.git
    cd test-task-django-uptrader
    ```

2. Установите зависимости и выполните миграции:
    ```bash
    poetry install
    python manage.py migrate
    python manage.py createsuperuser
    ```

3. Запустите сервер:
    ```bash
    python manage.py runserver
    ```

4. Откройте в браузере:
    ```
    http://127.0.0.1:8000/
    ```

### Запуск с Docker

1. Соберите и запустите контейнер:
    ```bash
    docker-compose up -d
    ```

2. Откройте в браузере:
    ```
    http://localhost:18000/
    ```

## Использование

- Добавляйте меню и пункты меню в Django-админке.
- Для отображения меню используйте template tag:
    ```django
    {% load main_tags %}
    {% draw_menu 'main_menu' %}
    ```

## Структура проекта

- `config/` — настройки Django
- `main/` — приложение с моделями меню, шаблонами и тегами
- `templates/main/` — шаблоны для меню
- `Dockerfile` и `docker-compose.yml` — для контейнеризации
- `pyproject.toml` и `poetry.lock` — зависимости проекта