# coding: utf8

from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_geoip.models import IpRange

from libs.models import CreateUpdate, ActiveState, ActiveManager


class Request(CreateUpdate, ActiveState):
    """Customers' requests"""

    phone = models.CharField(_('phone'), max_length=20)
    name = models.CharField(_('name'), max_length=512)
    email = models.CharField(_('email'), max_length=128, blank=True)
    ip = models.GenericIPAddressField(_('IP address'), blank=True, null=True)
    city = models.CharField(_('city'), max_length=255, blank=True)
    range = models.ForeignKey(IpRange, verbose_name=_('IP range'), blank=True, null=True)

    objects = models.Manager()
    objects_active = ActiveManager()

    class Meta(object):
        ordering = ['-pk']
        verbose_name = _('request')
        verbose_name_plural = _('requests')

    def __str__(self):
        return '{} #{}'.format(_('request'), self.pk)

    def set_city(self):
        try:        
            self.range = IpRange.objects.by_ip(self.ip)
            self.city = self.range.city.name
            return self.range
        except IpRange.DoesNotExist:
            return None
