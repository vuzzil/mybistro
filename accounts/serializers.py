from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import BistroUser


class BistroTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    For JWT Auth
    """

    @classmethod
    def get_token(cls, user):
        token = super(BistroTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['theme'] = user.theme
        return token


class BistroUserSerializer(serializers.ModelSerializer):
    """
    For login/signup use
    """
    email = serializers.EmailField(
        required=True
    )
    username = serializers.CharField()
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = BistroUser
        fields = ('email', 'username', 'password', 'theme' , 'is_staff', 'is_admin')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)  # as long as the fields are the same, we can just use this
        if password is not None:
            instance.set_password(password)
        # Add default theme=light
        instance.theme='light'
        instance.save()
        return instance

