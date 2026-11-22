from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=50,
        unique=True,
    )
    tg_chat_id = models.CharField(
        blank=True, null=True, max_length=100, verbose_name="ID телеграм чата"
    )
