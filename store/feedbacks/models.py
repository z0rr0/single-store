# coding: utf8
from logging import getLogger

from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_geoip.models import IpRange

from libs.models import CreateUpdate, ActiveState, ActiveManager
from products.models import Product


logger = getLogger(__name__)


class Request(CreateUpdate, ActiveState):
    """Customers' requests"""

    phone = models.CharField(_('phone'), max_length=20)
    name = models.CharField(_('name'), max_length=512)
    email = models.CharField(_('email'), max_length=128, blank=True)
    ip = models.GenericIPAddressField(_('IP address'), blank=True, null=True)
    city = models.CharField(_('city'), max_length=255, blank=True)
    range = models.ForeignKey(IpRange, verbose_name=_('IP range'), blank=True, null=True)
    product = models.ForeignKey(Product, verbose_name=_('product'), blank=True, null=True)
    comment = models.TextField(_('comment'), blank=True)

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
