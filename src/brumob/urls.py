from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^data/route/(?P<route>.*\.geojson)$', views.download_route, name='downloads'),
    url(r'^data/output/(?P<route>.*\.geojson)$', views.download_output, name='downloads'),
    url(r'^data/network.geojson$', views.download_network, name='downloads')
]
