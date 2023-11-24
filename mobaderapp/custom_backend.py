from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class MobileBackend(ModelBackend):
    def authenticate(self, request, mobile=None, password=None, **kwargs):
        user_model = get_user_model()

        try:
            user = user_model.objects.get(mobile=mobile)
        except user_model.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
