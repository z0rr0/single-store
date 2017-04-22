# coding: utf-8
from decimal import Decimal
from unittest.mock import patch

from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase, override_settings

from feedbacks.models import Request, EmailTemplate
from feedbacks.views import request_email
from products.models import Category, Product


class TestEmail(TestCase):

    def setUp(self):
        self.tpl_request = EmailTemplate.objects.create(
            name='test',
            is_basic=True,
            assignment=EmailTemplate.ASSIGNMENT_REQUEST,
            subject='subject',
            body='your name is {{ request.name }}.',
            body_html='your name is <b>{{ request.name }}</b>.',
        )
        self.tpl_seller = EmailTemplate.objects.create(
            name='test',
            is_basic=True,
            assignment=EmailTemplate.ASSIGNMENT_SELLER,
            subject='subject',
            body='request from {{ request.name }}.',
            body_html='request from <b>{{ request.name }}</b>.',
        )

    @override_settings(SEND_EMAIL_CONFIRMATION=True)
    def test_text_notification(self):
        r = Request(
            name='Adam',
            phone='123',
            email='test@localhost',
        )
        request_email(r)
        self.assertEqual(len(mail.outbox), 2)

        email_seller = mail.outbox[0]
        email_request = mail.outbox[1]

        bodies = {'your name is Adam.', 'request from Adam.'}
        sent_bodies = {email_seller.body, email_request.body}
        self.assertEqual(bodies, sent_bodies)

    @override_settings(SEND_EMAIL_CONFIRMATION=True)
    def test_html_notification(self):
        r = Request(
            name='Adam',
            phone='123',
            email='test@localhost',
        )
        self.tpl_seller.method = EmailTemplate.METHOD_HTML
        self.tpl_request.method = EmailTemplate.METHOD_HTML
        self.tpl_seller.save()
        self.tpl_request.save()

        request_email(r)
        self.assertEqual(len(mail.outbox), 2)

        email_seller = mail.outbox[0]
        email_request = mail.outbox[1]

        bodies = {'your name is <b>Adam</b>.', 'request from <b>Adam</b>.'}
        sent_bodies = {email_seller.body, email_request.body}
        self.assertEqual(bodies, sent_bodies)

    @override_settings(SEND_EMAIL_CONFIRMATION=True)
    def test_mixed_notification(self):
        r = Request(
            name='Adam',
            phone='123',
            email='test@localhost',
        )
        self.tpl_seller.method = EmailTemplate.METHOD_TEXT
        self.tpl_request.method = EmailTemplate.METHOD_HTML
        self.tpl_seller.save()
        self.tpl_request.save()

        request_email(r)
        self.assertEqual(len(mail.outbox), 2)

        email_seller = mail.outbox[0]
        email_request = mail.outbox[1]

        bodies = {'your name is <b>Adam</b>.', 'request from Adam.'}
        sent_bodies = {email_seller.body, email_request.body}
        self.assertEqual(bodies, sent_bodies)


class TestHandle(TestCase):
    URL = reverse('handle')

    def setUp(self):
        category = Category.objects.create(name='test')
        self.product = Product.objects.create(
            name='test',
            category=category,
            price=Decimal('100')
        )

    @patch('feedbacks.views.request_email')
    def test_failed_handle(self, mock):
        resp = self.client.get(self.URL)
        self.assertEqual(resp.status_code, 405)

        resp = self.client.post(self.URL)
        self.assertEqual(resp.status_code, 400)
        self.assertIsNotNone(resp.json().get('name'))
        self.assertIsNotNone(resp.json().get('phone'))

        resp = self.client.post(self.URL, {'name': 'test'})
        self.assertEqual(resp.status_code, 400)
        self.assertIsNone(resp.json().get('name'))
        self.assertIsNotNone(resp.json().get('phone'))

        resp = self.client.post(self.URL, {'name': 'test', 'phone': 'test', 'product': '0'})
        self.assertEqual(resp.status_code, 400)
        self.assertIsNotNone(resp.json().get('product'))

        resp = self.client.post(self.URL, {'name': 'test', 'phone': 'test', 'email': 'bad'})
        self.assertEqual(resp.status_code, 400)
        self.assertIsNotNone(resp.json().get('email'))

    @patch('feedbacks.views.request_email')
    def test_valid_handle(self, mock):
        data = {
            'name': 'test',
            'phone': '8(800)100-12-34',
        }
        count = Request.objects.count()

        resp = self.client.post(self.URL, data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Request.objects.count(), count + 1)

        data['product'] = self.product.id
        resp = self.client.post(self.URL, data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Request.objects.count(), count + 2)
