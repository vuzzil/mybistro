from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions

from django.contrib.auth import get_user_model
from .serializers import BistroUserSerializer, BistroTokenObtainPairSerializer

#import urllib.parse


# Create your views here.
"""
For JWT Auth ,add custom BistroUser.theme attribute instead
"""


class ObtainTokenPairWithThemeView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = BistroTokenObtainPairSerializer



@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def bistrouser_create(request):
    serializer = BistroUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        if user:
            json = serializer.data
            return Response(json, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def bistrouser_detail(request):
    if request.method == 'GET':
        UserModel = get_user_model()

        try:
            user_id = request.user.id
            user = UserModel.objects.get(pk=user_id)
            if user:
                serializer = BistroUserSerializer(user)
                return JsonResponse(serializer.data)
        except UserModel.DoesNotExist:
            return JsonResponse('無此使用者:'+user_id, status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse('error', status=status.HTTP_400_BAD_REQUEST)

