from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User


class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        
        try:
            if email==None:
                email = kwargs.get('username')              #Django Admin Page:use username field
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None
        else:
            #print('found user:' + str(user))
            if user.check_password(password):
                return user
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
