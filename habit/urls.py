from django.urls import path

from habit.views import (HabitCreateAPIView, HabitDestroyAPIView,
                         HabitListAPIView, HabitRetrieveAPIView,
                         HabitUpdateAPIView, PublicHabitListAPIView)

app_name = "habit"
urlpatterns = [
    path("habit_list/", HabitListAPIView.as_view(), name="habit_list"),
    path(
        "public_habit_list/", PublicHabitListAPIView.as_view(), name="public_habit_list"
    ),
    path("create/", HabitCreateAPIView.as_view(), name="habit_create"),
    path("update/<int:pk>/", HabitUpdateAPIView.as_view(), name="habit_update"),
    path("<int:pk>/destroy/", HabitDestroyAPIView.as_view(), name="habit_delete"),
    path("<int:pk>/", HabitRetrieveAPIView.as_view(), name="habit_detail"),
]
