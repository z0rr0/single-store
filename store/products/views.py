# coding: utf8

from logging import getLogger

from django.http import HttpRequest
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from products.models import Product

logger = getLogger(__name__)


# @cache_page(30 * 60)
def index(request: HttpRequest):
    products = Product.objects.all()
    context = {'a': 1, 'b': 'Hi All!', 'products': products}
    return render(request, 'products/index.html', context)
