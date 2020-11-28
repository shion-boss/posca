from __future__ import absolute_import, unicode_literals
from django.http import HttpResponse
from celery import shared_task
from .models import Widget
from posca.celery import app
import time
from django_celery_results.models import TaskResult


@app.task
def add(x, y):
    return x + y

from celery.decorators import periodic_task
from datetime import timedelta

@periodic_task(run_every=timedelta(seconds=10000))
def test_task():
    Widget(name='こんにた').save()
    return 'okだよ'


@app.task(name='task_number_one')
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
