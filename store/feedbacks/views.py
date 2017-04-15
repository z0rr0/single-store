# coding: utf-8

from smtplib import SMTPException

from django.conf import settings
from django.core import mail
from django.template import Context, Template

from feedbacks.models import Request, EmailTemplate


def request_email(request: Request):
    """It sends emails about requests"""
    context = Context({'product': request.product, 'request': request})
    seller_tpl = EmailTemplate.template_for(EmailTemplate.ASSIGNMENT_SELLER)
    seller_body = Template(seller_tpl.body).render(context)
    seller_body_html = Template(seller_tpl.body_html).render(context)
    messages = [
        (seller_tpl, seller_body, seller_body_html, settings.DEFAULT_FROM_EMAIL, settings.SELLERS_EMAILS)
    ]
    if request.email:
        request_tpl = EmailTemplate.template_for(EmailTemplate.ASSIGNMENT_REQUEST)
        request_body = Template(request_tpl.body).render(context)
        request_body_html = Template(request_tpl.body_html).render(context)
        messages.append(
            (request_tpl, request_body, request_body_html, settings.DEFAULT_FROM_EMAIL, [request.email])
        )
    with mail.get_connection() as connection:
        for tpl, body, body_html, from_email, to_emails in messages:
            if tpl.is_multipart:
                message = mail.EmailMultiAlternatives(
                    subject=tpl.subject,
                    body=body,
                    from_email=from_email,
                    to=to_emails,
                    connection=connection,
                )
                message.attach_alternative(body_html, 'text/html')
            else:
                email_body = body if tpl.is_text else body_html
                message = mail.EmailMessage(
                    subject=tpl.subject,
                    body=email_body,
                    from_email=from_email,
                    to=to_emails,
                    connection=connection,
                )
                if tpl.is_html:
                    message.content_subtype = 'html'
            message.send()
