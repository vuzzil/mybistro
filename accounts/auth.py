from django.contrib.auth.backends import BaseBackend
from datetime import datetime
from .models import BistroUser


class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = BistroUser
        
        try:
            if email==None:
                email = kwargs.get('username')              #Django Admin Page:use username field
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                user.last_login = datetime.now()
                user.is_authenticated = True
                user.save()
                #print('user saved:' + str(user))

                return user
        return None

    def get_user(self, user_id):
        UserModel = BistroUser
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
