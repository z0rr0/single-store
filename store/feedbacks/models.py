# coding: utf-8
from logging import getLogger

from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _

from django_geoip.models import IpRange

from libs.models import CreateUpdate, ActiveState, ActiveManager


logger = getLogger(__name__)


class Request(CreateUpdate, ActiveState):
    """Customers' requests"""
    VALIDATION_WAITING = 'waiting'
    VALIDATION_CONFIRMED = 'confirmed'
    VALIDATION_REJECTED = 'rejected'
    VALIDATION_HANDLED = 'handled'

    VALIDATION_CHOICES = (
        (VALIDATION_WAITING, _('waiting')),
        (VALIDATION_CONFIRMED, _('confirmed')),
        (VALIDATION_HANDLED, _('rejected')),
        (VALIDATION_REJECTED, _('handled')),
    )

    phone = models.CharField(_('phone'), max_length=20)
    name = models.CharField(_('name'), max_length=512)
    email = models.CharField(_('email'), max_length=128, blank=True)
    ip = models.GenericIPAddressField(_('IP address'), blank=True, null=True)
    city = models.CharField(_('city'), max_length=255, blank=True)
    product = models.ForeignKey('products.Product', verbose_name=_('product'), blank=True, null=True)
    validation = models.CharField(
        _('validation'), max_length=32, choices=VALIDATION_CHOICES, default=VALIDATION_WAITING, db_index=True
    )
    comment = models.TextField(_('comment'), blank=True)
    internal_comment = models.TextField(_('internal comment'), blank=True)

    objects = models.Manager()
    objects_active = ActiveManager()

    class Meta(object):
        ordering = ['-pk']
        verbose_name = _('request')
        verbose_name_plural = _('requests')

    def __str__(self):
        return '{} #{}'.format(_('request'), self.pk)

    def save(self, *args, **kwargs):
        if self.ip:
            try:
                self.range = IpRange.objects.by_ip(self.ip)
                self.city = self.range.city.name
            except (IpRange.DoesNotExist, AttributeError):
                logger.warning('unknown ip address: %s', self.ip)
        super(Request, self).save(*args, **kwargs)


class EmailTemplate(CreateUpdate):
    """Email template for customers"""
    METHOD_TEXT = 'text'
    METHOD_HTML = 'html'
    METHOD_MULTIPART = 'multipart'
    METHOD_CHOICES = (
        (METHOD_TEXT, _('plain text')),
        (METHOD_HTML, _('html')),
        (METHOD_MULTIPART, _('multipart content')),
    )

    ASSIGNMENT_REQUEST = 'request'
    ASSIGNMENT_SELLER = 'seller'
    ASSIGNMENT_CHOICES = (
        (ASSIGNMENT_REQUEST, _('request confirmation')),
        (ASSIGNMENT_SELLER, _('seller notification')),
    )

    name = models.CharField(_('name'), max_length=255)
    is_basic = models.BooleanField(
        _('basic'), default=False, help_text=_('basic template (can be only one for every assignment)')
    )
    method = models.CharField(_('method'), max_length=32, default=METHOD_TEXT, choices=METHOD_CHOICES, db_index=True)
    assignment = models.CharField(
        _('assignment'), max_length=32, default=ASSIGNMENT_REQUEST, choices=ASSIGNMENT_CHOICES, db_index=True
    )
    subject = models.CharField(_('subject'), max_length=255)
    body = models.TextField(_('body'), blank=True)
    body_html = models.TextField(_('HTML body'), blank=True)

    class Meta(object):
        ordering = ['name']
        verbose_name = _('email template')
        verbose_name_plural = _('email templates')

    def __str__(self):
        return self.name

    @transaction.atomic()
    def save(self, *args, **kwargs):
        if self.is_basic:
            # turn off other basic one
            EmailTemplate.objects.filter(is_basic=True, assignment=self.assignment).update(is_basic=False)
        super(EmailTemplate, self).save(*args, **kwargs)

    @classmethod
    def template_for(cls, assignment):
        return cls.objects.get(is_basic=True, assignment=assignment)

    @property
    def is_text(self):
        return self.method == self.METHOD_TEXT

    @property
    def is_html(self):
        return self.method == self.METHOD_HTML

    @property
    def is_multipart(self):
        return self.method == self.METHOD_MULTIPART
