from rest_framework import serializers
from bistro.models import BistroMenu

class BistroMenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = BistroMenu
        fields = ('id',
                  'menuid',
                  'label',
                  'title',
                  'price',
                  'desc',
                  'image')
