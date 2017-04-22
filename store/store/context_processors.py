# coding: utf-8

from django.core.cache import cache
from django.http import HttpRequest

from feedbacks.models import Contact
from products.models import Category


def categories(request: HttpRequest):
    """
    Returns products' categories.
    """
    key = 'categories'
    timeout = 30 * 60

    objects = cache.get(key)
    if not objects:
        objects = list(Category.objects.all())
        cache.set(key, objects, timeout)
    return {'categories': objects}


def search(request: HttpRequest):
    """
    Returns searched value.
    """
    return {'search_value': request.GET.get('search') or ''}


def contact_details(request: HttpRequest):
    """
    Returns searched value.
    """
    key = 'contact'
    timeout = 15 * 60

    contact = cache.get(key)
    if not contact:
        contact = Contact.objects.filter(is_basic=True).first()
        cache.set(key, contact, timeout)
    return {'contract': contact}
