from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^data/route/(?P<route>.*\.geojson)$', views.downloadRouteItem, name='downloads'),
    url(r'^data/output/(?P<route>.*\.geojson)$', views.downloadDifferenceItem, name='downloads'),
    url(r'^data/network.geojson$', views.downloadNetwork, name='downloads')
]
