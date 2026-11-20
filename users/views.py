from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from users.models import CustomUser
from users.serializers import CustomUsersSerializer


class CustomUserCreateAPIView(CreateAPIView):
    """контроллер регистрации пользователя"""

    serializer_class = CustomUsersSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
