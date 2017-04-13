# coding: utf-8

from logging import getLogger

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpRequest
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from products.models import Product

logger = getLogger(__name__)
PRODUCT_PAGE_SIZE = 8


@cache_page(15 * 60)
def index(request: HttpRequest):
    page = request.GET.get('page')
    search = request.GET.get('search')

    products_qs = Product.objects_active.all()
    if search:
        products_qs = products_qs.filter(name__icontains=search)
    paginator = Paginator(products_qs, PRODUCT_PAGE_SIZE)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {'a': 1, 'b': 'Hi All!', 'products': products}
    return render(request, 'products/index.html', context)
