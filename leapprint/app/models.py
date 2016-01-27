from __future__ import unicode_literals

# Create your models here.

from django.db import models

STATUSCHOICES = (
    ('new', 'New'),
    ('processed', 'Processed'),
    ('printed', 'Printed'),
)


class Order(models.Model):
    order_id = models.CharField(max_length=32, primary_key=True)
    status = models.CharField(max_length=16, choices=STATUSCHOICES, default=STATUSCHOICES[0][0])
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    data = models.TextField()

    class Meta:
        ordering = ('created',)


class Setting(models.Model):
    key = models.CharField(max_length=32, primary_key=True)
    value = models.TextField()


class File(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    path = models.FileField()

    class Meta:
        ordering = ('created',)


