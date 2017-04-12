# coding: utf8

from decimal import Decimal, ROUND_UP, getcontext


CONTEXT = getcontext()
CONTEXT.rounding = ROUND_UP


def round_money(value: Decimal, digits=2):
    assert digits >= 0
    return value.quantize(Decimal(10) ** -digits, context=CONTEXT)