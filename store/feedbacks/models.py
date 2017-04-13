# coding: utf-8
from logging import getLogger

from django.db import models
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
