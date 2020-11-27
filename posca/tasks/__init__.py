from igposca.celery import app
from ..models import taged_data,posca_point

@app.task()
def add_numbers(a, b):
    print('Request: {}'.format(a + b))
    models.taged_data(igname='test',top_img_url='a',main_img_url='b',text='',page_url='https://abe').save()
    return a + b

#from posca.tasks import add_numbers
