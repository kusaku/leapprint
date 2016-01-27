import datetime
import time

from rest_framework.serializers import ModelSerializer, DateTimeField

from models import Order, Setting, File


class TimestampField(DateTimeField):

    def to_internal_value(self, value):
        return self.enforce_timezone(datetime.datetime.fromtimestamp(
            int(value) / 1000
        ))

    def to_representation(self, value):
        return time.mktime(value.timetuple()) * 1000


class OrderSerializer(ModelSerializer):
    created = TimestampField(read_only=False)
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
