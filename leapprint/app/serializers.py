import time

from rest_framework.serializers import ModelSerializer, DateTimeField

from models import Order, Setting, File


class TimestampField(DateTimeField):
    def to_representation(self, value):
        return time.mktime(value.timetuple())


class OrderSerializer(ModelSerializer):
    created = TimestampField(read_only=True)
    modified = TimestampField(read_only=True)

    class Meta:
        model = Order
        fields = ('order_id', 'status', 'data', 'created', 'modified')


class SettingSerializer(ModelSerializer):
    class Meta:
        model = Setting
        fields = ('key', 'value')


class FileSerializer(ModelSerializer):
    created = TimestampField(read_only=True)

    class Meta:
        model = File
