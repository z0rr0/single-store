# coding: utf-8
from django.core.urlresolvers import reverse
from django.test import TestCase


class TestIndex(TestCase):

    def test_index_available(self):
        url = reverse('index')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
