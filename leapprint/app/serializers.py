from rest_framework.serializers import ModelSerializer

from models import Order, Setting, File


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order


class SettingSerializer(ModelSerializer):
    class Meta:
        model = Setting
        fields = ('key', 'value')


class FileSerializer(ModelSerializer):
    class Meta:
        model = File
