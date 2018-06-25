from django.conf.urls import url
from . import views 

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^dashboard$', views.dash),
    url(r'^wish_items/(?P<id>\d+)$', views.show),
    url(r'^logout$', views.logout),
    url(r'^delete$', views.delete),
    url(r'^remove/(?P<id>\d+)$', views.remove),
    url(r'^create$', views.create),
    url(r'^add$', views.add),
    url(r'^create_item$', views.create_item),
]     