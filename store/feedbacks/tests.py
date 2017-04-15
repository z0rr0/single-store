# coding: utf-8
from django.core import mail
from django.test import TestCase

from feedbacks.models import Request, EmailTemplate
from feedbacks.views import request_email


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
