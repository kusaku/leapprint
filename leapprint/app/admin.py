# Register your models here.

from django.contrib import admin

from models import Order, Setting, File


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    pass


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    pass
