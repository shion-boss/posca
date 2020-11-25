from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index_view,name='index'),
    path('2/',views.index2_view,name='index2'),
    path("ajax/",views.test_ajax_response,name='ajax'),
    path('st/',views.search_tags_ajax_view,name='st'),
    path('ajax_test/',views.ajax_test_view,name='ajax_test'),
]
