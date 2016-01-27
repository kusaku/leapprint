from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.parsers import FormParser, MultiPartParser

from django.http.response import Http404

from serializers import OrderSerializer, SettingSerializer, FileSerializer
from models import Order, Setting, File


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

    def retrieve(self, request, *args, **kwargs):
        try:
            return super(OrderViewSet, self).retrieve(request, *args, **kwargs)

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


class SettingViewSet(ListModelMixin, GenericViewSet):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        data = {item['key']: item['value'] for item in serializer.data}

        return Response(data)


class FileViewSet(ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        serializer.save(path=self.request.data.get('path'))

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
                'file': serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED, headers=headers)
