# Create your models here.
from __future__ import unicode_literals

from django.db import models


STATUSCHOICES = (
    ('new', 'New'),
    ('processed', 'Processed'),
    ('printed', 'Printed'),
)

class Order(models.Model):
    order_id = models.CharField(max_length=32, unique=True)
    status = models.CharField(max_length=16, choices=STATUSCHOICES, default=STATUSCHOICES[0][0])
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    data = models.TextField(blank=True, null=True)
    file = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('created',)


class Setting(models.Model):
    key = models.CharField(max_length=32, unique=True)
    value = models.TextField()
