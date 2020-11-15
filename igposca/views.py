from django.shortcuts import render

# Create your views here.


def index_view(request):
    params={
        'a':'b',
    }
    return render(request,'igposca/index.html',params)
