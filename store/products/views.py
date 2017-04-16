# coding: utf-8

from logging import getLogger

from django.conf import settings
from django.db.models import Count
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpRequest
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from feedbacks.models import Request
from products.models import Product, Category


logger = getLogger(__name__)
DEFAULT_POPULAR_SIZE = 3
DEFAULT_CATEGORIES_ROW = 3


def _popular_products(size=DEFAULT_POPULAR_SIZE):
    qs = Request.objects.filter(
        product__isnull=False
    ).values('product_id').annotate(count=Count('id')).order_by('-count')[:size]

    popular_products, other_products = [p['product_id'] for p in qs], []
    if len(qs) < size:
        other_products = list(
            Product.objects.exclude(id__in=popular_products).values_list('id', flat=True)[:(size-len(qs))]
        )
    product_ids = popular_products + other_products
    return Product.objects.filter(id__in=product_ids)


@cache_page(30 * 60)
def index(request: HttpRequest):
    categories = Category.objects.all()
    category_rows = []
    for i in range(0, len(categories), DEFAULT_CATEGORIES_ROW):
        category_rows.append(categories[i:i+DEFAULT_CATEGORIES_ROW])
    return render(
        request,
        'products/index.html',
        {
            'category_rows': category_rows,
            'popular_products': _popular_products(),
        }
    )


@cache_page(15 * 60)
def search(request: HttpRequest):
    page = request.GET.get('page')
    name = request.GET.get('search')
    category_id = request.GET.get('category')

    products_qs, category = Product.objects_active.all(), None
    if name:
        products_qs = products_qs.filter(name__icontains=name)
    if category_id:
        try:
            category = Category.objects.get(pk=category_id)
            products_qs = products_qs.filter(category=category)
        except Category.DoesNotExist:
            pass
    paginator = Paginator(products_qs, settings.PRODUCT_PAGE_SIZE)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request, 'products/index.html', {'category': category, 'products': products})
