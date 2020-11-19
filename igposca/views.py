from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index_view(request):
    params={
        'a':'b',
    }
    return render(request,'igposca/index.html',params)


def webhooks_view(request):
    response = HttpResponse(status=200)
    return response
