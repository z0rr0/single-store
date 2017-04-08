# coding: utf8

from logging import getLogger

from django.http import HttpRequest
from django.shortcuts import render

logger = getLogger(__name__)


def index(request: HttpRequest):
    context = {'a': 1, 'b': 'Hi All!'}
    return render(request, 'products/index.html', context)
