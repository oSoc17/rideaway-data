from django.conf.urls import url

from . import views

urlpatterns = [
     url(r'^$',views.index,name='index'),
     url(r'^download/$',views.download,name='downloads'),
]
