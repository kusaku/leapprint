from rest_framework.serializers import HyperlinkedModelSerializer

from models import Order, Setting, File


class OrderSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Order


class SettingSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Setting
        fields = ('key', 'value')


class FileSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = File
