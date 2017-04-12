# coding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _


class CreateUpdate(models.Model):
    """Common abstract class for created/updated datetimes"""
    modified = models.DateTimeField(_('modified'), auto_now=True, editable=False)
    created = models.DateTimeField(_('created'), auto_now_add=True, editable=False)

    class Meta(object):
        abstract = True


class ActiveState(models.Model):
    """Abstract class for models with states"""
    STATUS_ACTIVE = 'active'
    STATUS_HIDE = 'hide'

    STATUSES = (
        ('active', _('Active')),
        ('hide', _('Hidden')),
    )
    status = models.CharField(_('status'), max_length=64, default=STATUS_ACTIVE, choices=STATUSES, db_index=True)

    class Meta(object):
        abstract = True


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super(ActiveManager, self).get_queryset().filter(status=ActiveState.STATUS_ACTIVE)
