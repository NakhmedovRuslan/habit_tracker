from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from users.models import CustomUser


class Habit(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255)
    pleasant_habit = models.BooleanField(default=False)  # приятная прмвычка
    related_habit = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='related_to')  # связанная привычка
    period = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(7)])
    award = models.CharField(max_length=255, blank=True)
    time_to_complete = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(120)])
    is_public = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def __str__(self):
        return f"Я буду {self.action} в {self.time} в {self.location}"

    def clean(self):
        if self.pleasant_habit and self.related_habit:
            raise ValidationError("Приятная привычка не может иметь связанную привычку")
        elif not self.pleasant_habit and self.related_habit and self.award:
            raise ValidationError("Нельзя одновременно указывать связанную привычку и вознаграждение")
        elif self.pleasant_habit and self.award:
            raise ValidationError("У вас уже есть вознаграждения- приятная привычка")
        elif self.related_habit and not self.related_habit.pleasant_habit:
            raise ValidationError("Связанная привычка должна быть приятной")
