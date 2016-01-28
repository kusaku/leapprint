# Register your models here.

from django.contrib import admin

from models import Order, Setting


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'status', 'data', 'created', 'modified')
    list_filter = ('order_id', 'status', 'data', 'created', 'modified')


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')
    list_filter = ('key', 'value')
