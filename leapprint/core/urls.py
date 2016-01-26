"""leapprint URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from rest_framework import routers

from app import views

# router = routers.DefaultRouter(trailing_slash=False)
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)
# router.register(r'orders', views.OrderViewList)
# router.register(r'^orders/(?P<pk>[0-9]+)/$', views.OrderViewDetail)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^', include(router.urls)),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    # url(r'^orders2/$', views.OrderViewSet2.as_view()),
    url(r'^orders/$', views.OrderViewList.as_view()),
    url(r'^orders/(?P<pk>[0-9]+)/$', views.OrderViewDetail.as_view())
]



