# coding: utf-8

from django.conf.urls import url

from products import views


urlpatterns = [
    url(r'^$', views.search, name='search'),
    url(r'^info/(?P<pk>\d+)/?$', views.info, name='info'),
]
