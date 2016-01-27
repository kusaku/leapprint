from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse

from django.http.response import Http404

from serializers import OrderSerializer
from models import Order


@api_view(('GET',))
def api_root(request, format=None):
    return Response({'orders': reverse('orders-list', request=request, format=format)})


class OrderViewList(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
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


class OrderViewDetail(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        try:
            return super(OrderViewDetail, self).get(request, *args, **kwargs)

        except Http404 as e:
            data = {
                'status': 0,
                'error': e.message,
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
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

    def delete(self, request, *args, **kwargs):
        try:
            return super(OrderViewDetail, self).delete(request, *args, **kwargs)

        except Http404 as e:
            data = {
                'status': 0,
                'error': e.message,
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
