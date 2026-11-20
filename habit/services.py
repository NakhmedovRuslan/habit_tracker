import requests

from config.settings import TG_TOKEN


def send_telegram_message(chat_id, message):
    params = {"chat_id": chat_id, "text": message}
    requests.get(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage", params=params)
