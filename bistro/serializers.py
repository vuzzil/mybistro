from rest_framework_mongoengine import serializers
from bistro.models import BistroMenu

class BistroMenuSerializer(serializers.DocumentSerializer):

    class Meta:
        model = BistroMenu
        fields = ('id',
                  'menuid',
                  'label',
                  'title',
                  'price',
                  'desc',
                  'image',
                  'date_modified')
