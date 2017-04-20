# coding: utf-8
from decimal import Decimal

from django.core.urlresolvers import reverse
from django.test import TestCase

from libs.utils import batch_split
from products.models import Product, Category


class TestIndex(TestCase):

    def test_index_available(self):
        url = reverse('index')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_search_available(self):
        url = reverse('search')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_info_available(self):
        category = Category.objects.create(name='test')
        product = Product.objects.create(
            name='test',
            category=category,
            price=Decimal('100')
        )
        url = reverse('info', args=(product.pk,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        url = reverse('info', args=(9999,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)


class TestUtils(TestCase):

    def test_batch_split(self):
        examples = {
            tuple(): [],
            (1,): [(1,)],
            (1, 2): [(1, 2)],
            (1, 2, 3): [(1, 2), (3,)],
            (1, 2, 3, 4): [(1, 2), (3, 4)],
            (1, 2, 3, 4, 5): [(1, 2), (3, 4), (5,)],
            (1, 2, 3, 4, 5, 6): [(1, 2), (3, 4), (5, 6)],
        }
        for item, expected in examples.items():
            self.assertEqual(batch_split(item, 2), expected)
