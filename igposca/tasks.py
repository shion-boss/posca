from __future__ import absolute_import, unicode_literals
from .models import taged_data
from django.http import HttpResponse
from posca.celery import app

@app.task(name='task_number_one')
def some_task():
    taged_data(igname='test',top_img_url='a',main_img_url='b',text='',page_url='https://abe').save()
    global message
    message='tasks１完了です'
    return True


from posca.celery import app

@app.task(name='task_number_two')
def add_numbers():
    taged_data(igname='test',top_img_url='a',main_img_url='b',text='',page_url='https://abe').save()
    message='tasks2完了です'
    return True
