from __future__ import absolute_import, unicode_literals
from django.http import HttpResponse
from celery import shared_task
from .models import Widget
from posca.celery import app


@app.task
def add(x, y):
    return x + y

@shared_task
def test_task():
    message='aiueo'
    return message


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def count_widgets():
    return Widget.objects.count()


@shared_task
def rename_widget(widget_id, name):
    w = Widget.objects.get(id=widget_id)
    w.name = name
    w.save()
