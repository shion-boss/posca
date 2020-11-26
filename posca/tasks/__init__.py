from ..celery import app


@app.task()
def add_numbers(a, b):
    print('Request: {}'.format(a + b))
    return a + b

#from posca.tasks import add_numbers
