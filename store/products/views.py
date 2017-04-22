# coding: utf-8

from logging import getLogger
from urllib.parse import urlencode

from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, reverse
from django.views.decorators.cache import cache_page

from feedbacks.forms import RequestForm
from feedbacks.models import Request
from libs.utils import batch_split
from products.models import Product, Category


logger = getLogger(__name__)
DEFAULT_POPULAR_SIZE = 3
DEFAULT_CATEGORIES_ROW = 3
PRODUCT_ROW_SIZE = 2


def _popular_products() -> list:
    qs = Request.objects.filter(
        product__isnull=False
    ).values('product_id').annotate(count=Count('id')).order_by('-count')[:DEFAULT_POPULAR_SIZE]

    popular_products, other_products = [p['product_id'] for p in qs], []
    if len(qs) < DEFAULT_POPULAR_SIZE:
        other_products = list(
            Product.objects.exclude(
                id__in=popular_products
            ).values_list('id', flat=True)[:(DEFAULT_POPULAR_SIZE-len(qs))]
        )
    product_ids = popular_products + other_products

    classes = (
        ('first-slide', ' active'),
        ('second-slide', ''),
        ('third-slide', ''),
    )
    products = []
    for i, product in enumerate(Product.objects.filter(id__in=product_ids)):
        class_name, active = classes[i]
        products.append({'class': class_name, 'active': active, 'product': product})
    return products


@cache_page(30 * 60)
def index(request: HttpRequest) -> HttpResponse:
    category_rows = batch_split(Category.objects.all(), DEFAULT_CATEGORIES_ROW)
    return render(
        request,
        'products/index.html',
        {
            'category_rows': category_rows,
            'popular_products': _popular_products(),
        }
    )


@cache_page(15 * 60)
def search(request: HttpRequest) -> HttpResponse:
    page = request.GET.get('page')
    name_search = request.GET.get('search', '')
    category_id = request.GET.get('category', '')
    params = {'search': name_search, 'category': category_id}

    products_qs, category = Product.objects_active.all(), None
    if name_search:
        products_qs = products_qs.filter(name__icontains=name_search)
    if category_id:
        try:
            category = Category.objects.get(pk=category_id)
            products_qs = products_qs.filter(category=category)
        except Category.DoesNotExist:
            pass
    paginator = Paginator(products_qs, settings.PRODUCT_PAGE_SIZE)
    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)
    products_rows = batch_split(products_page, PRODUCT_ROW_SIZE)
    return render(
        request,
        'products/search.html',
        {
            'category': category,
            'products_page': products_page,
            'products_rows': products_rows,
            'name_search': name_search,
            'base_url': '{url}?{query}'.format(url=reverse('search'), query=urlencode(params)),
            'pages': range(1, paginator.num_pages+1)
        }
    )


@cache_page(15 * 60)
def info(request: HttpRequest, pk: int) -> HttpResponse:
    product = get_object_or_404(Product, pk=pk)
    form = RequestForm(initial={'product': product.id})
    return render(request, 'products/info.html', {'product': product, 'form': form})
