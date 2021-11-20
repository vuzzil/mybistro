from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import permissions
from rest_framework.parsers import JSONParser
from rest_framework import status
from .bistrolog import logging

from mongoengine import connect, disconnect
from .models import BistroMenu
from .serializers import BistroMenuSerializer


# Create your views here.
"""
For JWT Auth ,add custom BistroUser.theme attribute instead
"""


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def bistromenu_test(request):
    if request.method == 'GET':
        # connect(
        #     alias='bistrodb',
        #     db='bistrodb',
        #     host='mongodb://vincent:pass2021@localhost:27017/?authSource=bistrodb&authMechanism=SCRAM-SHA-256'
        # )
        # bistromenu = BistroMenu(menuid='A001', title='test')
        # bistromenu.save()

        menus = BistroMenu.objects.all()
        serializer = BistroMenuSerializer(menus, many=True)
        return JsonResponse(serializer.data, safe=False)

# data = []
# for doc in BistroMenu.objects().order_by('-price'):
#     print(doc.to_json())
#     data.append(doc.to_json())

# disconnect('bistrodb')

# return JsonResponse(data, safe=False)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def bistromenu_list(request):
    if request.method == 'GET':
        menus = BistroMenu.objects.all()

        menuid = request.GET.get('menuid', None)
        logging.debug("menuid=" + str(menuid))
        if menuid is not None:
            menus = menus.filter(menuid__icontains=menuid)
        type = request.GET.get('type', None)
        if type is not None:
            menus = menus.filter(menuid__startswith=type)
        sortprice = request.GET.get('sortprice', None)
        if sortprice is not None:
            field = 'price' if (sortprice == '1') else '-price'
            menus = menus.order_by(field)

        serializer = BistroMenuSerializer(menus, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        bistromenu_data = JSONParser().parse(request)
        serializer = BistroMenuSerializer(data=bistromenu_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def bistromenu_detail(request, pk):
    if request.method == 'GET':
        bistromenu = BistroMenu.objects.get(pk=pk)
        bistromenu_serializer = BistroMenuSerializer(bistromenu)
        return JsonResponse(bistromenu_serializer.data)
    elif request.method == 'PUT':
        bistromenu_data = JSONParser().parse(request)
        bistromenu_serializer = BistroMenuSerializer(BistroMenu, data=bistromenu_data)
        if bistromenu_serializer.is_valid():
            bistromenu_serializer.save()
            return JsonResponse(bistromenu_serializer.data)
        return JsonResponse(bistromenu_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        bistromenu = BistroMenu.objects.get(pk=pk)
        bistromenu.delete()
        return JsonResponse({'message': 'bistromenu was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
