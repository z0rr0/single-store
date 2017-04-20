# coding: utf-8
from django.core.urlresolvers import reverse
from django.test import TestCase

from libs.utils import batch_split


class TestIndex(TestCase):

    def test_index_available(self):
        url = reverse('index')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)


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
