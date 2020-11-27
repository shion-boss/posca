from __future__ import absolute_import, unicode_literals
from celery import task
from .models import taged_data
from django.http import HttpResponse

@task(name='task_number_one')
def some_task():
    taged_data(igname='test',top_img_url='a',main_img_url='b',text='',page_url='https://abe').save()
    return HttpResponse('tasks１完了です')


from igposca.celery import app

@app.task(name='task_number_two')
def add_numbers():
    taged_data(igname='test',top_img_url='a',main_img_url='b',text='',page_url='https://abe').save()
    return HttpResponse('tasks２完了です')
