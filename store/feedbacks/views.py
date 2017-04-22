# coding: utf-8
from logging import getLogger
from smtplib import SMTPException

from django.conf import settings
from django.core import mail
from django.http import HttpRequest, JsonResponse
from django.template import Context, Template
from django.views.decorators.http import require_POST

from feedbacks.forms import RequestForm
from feedbacks.models import Request, EmailTemplate


logger = getLogger(__name__)


def request_email(request: Request) -> None:
    """It sends emails about requests"""
    context = Context({'product': request.product, 'request': request})
    seller_tpl = EmailTemplate.template_for(EmailTemplate.ASSIGNMENT_SELLER)
    seller_body = Template(seller_tpl.body).render(context)
    seller_body_html = Template(seller_tpl.body_html).render(context)
    messages = [
        (seller_tpl, seller_body, seller_body_html, settings.DEFAULT_FROM_EMAIL, settings.SELLERS_EMAILS)
    ]
    if settings.SEND_EMAIL_CONFIRMATION and request.email:
        try:
            request_tpl = EmailTemplate.template_for(EmailTemplate.ASSIGNMENT_REQUEST)
            request_body = Template(request_tpl.body).render(context)
            request_body_html = Template(request_tpl.body_html).render(context)
        except EmailTemplate.DoesNotExist:
            logger.warning('not found users email template')
        else:
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


@require_POST
def handle(request: HttpRequest) -> JsonResponse:
    u"""It handles incoming customers' requests."""
    form = RequestForm(request.POST)
    if form.is_valid():
        form.save(commit=False)
        instance = form.instance
        instance.ip = request.META.get('REMOTE_ADDR')
        instance.save()
        try:
            request_email(instance)
            result = 'ok'
        except (EmailTemplate.DoesNotExist, SMTPException) as exc:
            logger.error('send request emails error: %s', exc, exc_info=True)
            result = 'nok'
        # anyway send successful status, because data is valid and saved
        result, status = {'result': result}, 200
    else:
        result, status = dict(form.errors), 400
    return JsonResponse(result, status=status)
