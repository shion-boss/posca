from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index_view,name='index'),
    path('webhooks/',views.webhooks_view,name='webhooks'),
]
