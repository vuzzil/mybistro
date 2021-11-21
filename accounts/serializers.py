from rest_framework_mongoengine import serializers
from rest_framework_simplejwt_mongoengine.serializers import TokenObtainPairSerializer
from .models import BistroUser
from bcrypt import hashpw, gensalt


class BistroTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    For JWT Auth
    """

    @classmethod
    def get_token(cls, user):
        #print('get_token user:' + str(user))
        token = super().get_token(user)

        # Add custom claims
        token['theme'] = user.theme
        return token


class BistroUserSerializer(serializers.DocumentSerializer):
    """
    For login/signup use
    """
    class Meta:
        model = BistroUser
        fields = '__all__'
        

    def create(self, validated_data):
        user = BistroUser(
            email = validated_data['email'],
            username = validated_data['username'],
            password = validated_data['password'],
            theme = '',
            staff = False,
            admin = False,
            is_authenticated = False,
        )
        #encode password
        hashed = hashpw(user.password.encode('utf8'), gensalt())
        user.password = hashed.decode('utf8')
        
        user.save()

        return user
