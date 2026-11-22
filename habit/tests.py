from datetime import time

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from habit.models import Habit


User = get_user_model()


class HabitTestCase(TestCase):

    def setUp(self):
        """Создание пользователя и привычки"""
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="testuser1",
            password="12345",
        )

        self.other_user = User.objects.create_user(
            username="testuser2",
            password="12345",
        )

        self.habit = Habit.objects.create(
            user=self.user,
            location="Дом",
            time=time(9, 0),
            action="Читать книгу",
            time_to_complete=60,
        )

    def test_habit_model(self):
        """тестирование модели и валидаторов привычки"""
        self.assertEqual(str(self.habit), "Я буду Читать книгу в 09:00:00 в Дом")

        self.habit.period = 8
        with self.assertRaises(ValidationError):
            self.habit.full_clean()

        self.habit.period = 1
        self.habit.time_to_complete = 121
        with self.assertRaises(ValidationError):
            self.habit.full_clean()

    def test_habit_list(self):
        """Тестирование получения списка своих привычек"""
        self.client.force_authenticate(user=self.user)

        response = self.client.get(reverse("habit:habit_list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_public_habit_list(self):
        """Тестирование получения списка публичных привычек"""
        Habit.objects.create(
            user=self.other_user,
            location="Парк",
            time=time(11, 0),
            action="Гулять",
            time_to_complete=60,
            is_public=True,
        )

        response = self.client.get(reverse("habit:public_habit_list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_create_habit(self):
        """Тестирование создания привычки"""
        self.client.force_authenticate(user=self.user)

        data = {
            "location": "Парк",
            "time": "12:00:00",
            "action": "Гулять",
            "time_to_complete": 60,
        }

        response = self.client.post(
            reverse("habit:habit_create"),
            data,
            format="json",
        )

        print(response.data)
        self.assertEqual(response.status_code, 201)

    def test_retrieve_habit(self):
        """Тестирование просмотра своей привычки"""
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse("habit:habit_detail", kwargs={"pk": self.habit.pk})
        )

        self.assertEqual(response.status_code, 200)

    def test_update_delete_and_permissions(self):
        """тестирование редактирования, удаления и доступа к чужой привычке"""
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            reverse("habit:habit_update", kwargs={"pk": self.habit.pk}),
            {"action": "Гулять"},
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.delete(
            reverse("habit:habit_delete", kwargs={"pk": self.habit.pk})
        )
        self.assertEqual(response.status_code, 204)

        other_habit = Habit.objects.create(
            user=self.other_user,
            location="Парк",
            time=time(12, 0),
            action="Гулять",
            time_to_complete=60,
        )

        response = self.client.get(
            reverse("habit:habit_detail", kwargs={"pk": other_habit.pk})
        )
        self.assertEqual(response.status_code, 404)