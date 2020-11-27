from __future__ import absolute_import, unicode_literals
from celery import task
from . import models
from django.http import HttpResponse

@task(name='task_number_one')
def some_task():
    models.taged_data(igname='test',top_img_url='a',main_img_url='b',text='',page_url='https://abe').save()
    return HttpResponse('tasks完了です')
