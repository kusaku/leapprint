from rest_framework import status, renderers
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from django.http.response import Http404

from serializers import OrderSerializer, SettingSerializer
from models import Order, Setting


class OrderViewSet(ModelViewSet):
    lookup_field = 'order_id'

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

        except ValidationError as e:
            data = {
                'status': 0,
                'error': ' '.join(['%s: %s' % (k, ', '.join(v)) for k, v in e.detail.items()]),
            }
            return Response(data, status=e.status_code)

        else:
            headers = self.get_success_headers(serializer.data)
            data = {
                'status': 1,
                'order': serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        data = serializer.data

        for item in data:
            kwargs = {'order_id': item['order_id']}
            item['file'] = reverse('order-file', request=request, kwargs=kwargs)

        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)

            data = serializer.data

            kwargs = {'order_id': data['order_id']}
            data['file'] = reverse('order-file', request=request, kwargs=kwargs)

            return Response(data)


        except Http404 as e:
            data = {
                'status': 0,
                'error': e.message,
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

        except ValidationError as e:
            data = {
                'status': 0,
                'error': ' '.join(['%s: %s' % (k, ', '.join(v)) for k, v in e.detail.items()]),
            }
            return Response(data, status=e.status_code)

        except Http404 as e:
            data = {
                'status': 0,
                'error': e.message,
            }
            return Response(data, status.HTTP_404_NOT_FOUND)

        else:
            data = {
                'status': 1,
                'order': serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        try:
            return super(OrderViewSet, self).destroy(request, *args, **kwargs)

        except Http404 as e:
            data = {
                'status': 0,
                'error': e.message,
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class PNGRenderer(renderers.BaseRenderer):
    media_type = 'image/png'
    format = 'png'
    charset = None
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        return data


class OrderFileViewSet(RetrieveModelMixin, GenericViewSet):
    lookup_field = 'order_id'
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    renderer_classes = (PNGRenderer,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data.get('file'))


class SettingViewSet(ListModelMixin, GenericViewSet):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        data = {item['key']: item['value'] for item in serializer.data}

        return Response(data)
