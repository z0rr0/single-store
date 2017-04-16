# coding: utf-8

from django.conf.urls import url

from products.views import search


urlpatterns = [
    url(r'^$', search, name='search'),
]
