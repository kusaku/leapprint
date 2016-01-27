import datetime
import time

from rest_framework.serializers import ModelSerializer, DateTimeField

from models import Order, Setting


class TimestampField(DateTimeField):
    def to_internal_value(self, value):
        try:
            return self.enforce_timezone(datetime.datetime.fromtimestamp(
                float(value) / 1000
            ))
        except ValueError:
            return None

    def to_representation(self, value):
        return '%d' % (time.mktime(value.timetuple()) * 1000)


class OrderSerializer(ModelSerializer):
    created = TimestampField(read_only=False)
    modified = TimestampField(read_only=True)

    class Meta:
        model = Order
        fields = ('order_id', 'status', 'data', 'created', 'modified', 'file')


class SettingSerializer(ModelSerializer):
    class Meta:
        model = Setting
        fields = ('key', 'value')
