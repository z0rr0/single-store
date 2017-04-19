# coding: utf-8

from decimal import Decimal, ROUND_UP, getcontext
from typing import Sized


CONTEXT = getcontext()
CONTEXT.rounding = ROUND_UP


def round_money(value: Decimal, digits=2) -> Decimal:
    assert digits >= 0
    return value.quantize(Decimal(10) ** (-digits), context=CONTEXT)


def batch_split(items: Sized, size: int) -> list:
    objects = []
    for i in range(0, len(items), size):
        objects.append(items[i:i+size])
    return objects
