from django.conf.urls import url

from . import views

urlpatterns = [
     url(r'^$',views.index,name='index'),
     url(r'^downloads/$',views.downloads,name='downloads'),
     url(r'^downloads/route/(?P<route>.*)/$',views.downloadRouteItem,name='downloads'),
     url(r'^downloads/difference/(?P<route>.*)/$',views.downloadDifferenceItem,name='downloads'),


]
