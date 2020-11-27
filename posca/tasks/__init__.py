from ..celery import app

@app.task()
def add_numbers(a, b):
    print('Request: {}'.format(a + b))
    print('いい感じだよ！おまえは天才')
    return a + b

#from posca.tasks import add_numbers
