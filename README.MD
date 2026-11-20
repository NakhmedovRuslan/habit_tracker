# Habit Tracker

Бэкенд-часть SPA-приложения для отслеживания полезных привычек.

## Возможности

- Регистрация и авторизация пользователей.
- Создание, просмотр, редактирование и удаление привычек.
- Просмотр **публичных** привычек других пользователей.
- Напоминания о привычках через Телеграм.
- Автоматическая отправка уведомлений с помощью Celery и Redis.

## Технологии

- Python
- Django
- Django REST Framework
- PostgreSQL
- Celery
- Redis
- Telegram Bot API

## Установка и запуск

1. Клонировать репозиторий:

```bash
git clone https://github.com/NakhmedovRuslan/habit_tracker.git
cd habit_tracker
```

2. Клонировать репозиторий:

```bash
poetry install
```

3. Создать файл .env и заполнить необходимые переменные окружения по примеру .env.template.

4. Выполнить миграции:
```bash
python manage.py migrate
```

5. Запустить сервер:
```bash
python manage.py runserver 
```

## Celery и Redis

Для работы уведомлений необходимо запустить Redis, Celery Worker и Celery Beat.

Worker:

```bash
celery -A config worker -l INFO --pool=solo
```

Beat:

```bash
celery -A config beat -l INFO
```

## Документация API

После запуска сервера документация доступна по адресу:

`http://127.0.0.1:8000/api/docs/`