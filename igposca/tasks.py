from __future__ import absolute_import, unicode_literals
from .models import taged_data
from django.http import HttpResponse
from posca.celery import app

@app.task(name='task_number_one')
def some_task():
    taged_data(igname='test',top_img_url='a',main_img_url='b',text='',page_url='https://abe').save()
    return HttpResponse('tasks１完了です')


@app.task(name='task_number_two')
def add_numbers():
    taged_data(igname='test',top_img_url='a',main_img_url='b',text='',page_url='https://abe').save()
    message='tasks2完了です'
    return HttpResponse(message)

from celery import shared_task
from .models import Widget


@shared_task
def add(x, y):
    return x + y

@shared_task
def text_task():
    taged_data(igname='test',top_img_url='a',main_img_url='b',text='',page_url='https://abe').save()
    message='tasks2完了です'
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
