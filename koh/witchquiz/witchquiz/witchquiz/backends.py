from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from witchquiz.models import UserToken

UserModel = get_user_model()

class TokenAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        userToken = UserToken.objects.filter(token=password)
        if len(userToken) != 1:
            return
        userToken = userToken[0]

        if self.user_can_authenticate(userToken.user):
            return userToken.user