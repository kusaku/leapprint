import datetime
import time
import base64

from rest_framework.serializers import ModelSerializer, DateTimeField, FileField

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


class BlobFileField(FileField):
    def to_internal_value(self, data):
        bindata = data.file.read()
        strdata = base64.encodestring(bindata)

        return strdata

    def to_representation(self, value):
        if not value:
            return None
        try:
            return base64.decodestring(value)
        except Exception as e:
            return e.message


class OrderSerializer(ModelSerializer):
    created = TimestampField(read_only=False)
    modified = TimestampField(read_only=True)
    file = BlobFileField()

    class Meta:
        model = Order
        fields = ('order_id', 'status', 'data', 'created', 'modified', 'file')


class SettingSerializer(ModelSerializer):
    class Meta:
        model = Setting
        fields = ('key', 'value')
