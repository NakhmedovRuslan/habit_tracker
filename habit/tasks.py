from celery import shared_task
from django.utils import timezone

from habit.models import Habit
from habit.services import send_telegram_message


@shared_task
def send_telegram_task(chat_id, message):
    send_telegram_message(chat_id, message)


@shared_task
def check_habits():
    current_time = timezone.localtime().time().replace(second=0, microsecond=0)

    habits = Habit.objects.filter(time=current_time)

    for habit in habits:
        if habit.user.tg_chat_id:
            message = f"Прпишло время выполнить {habit.action}"
            send_telegram_task.delay(habit.user.tg_chat_id, message)
