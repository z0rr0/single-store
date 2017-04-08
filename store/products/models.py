# coding: utf8

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
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


class Category(CreateUpdate):
    """Product categories"""
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    def __str__(self):
        return self.name

    class Meta(object):
        ordering = ['name']
        verbose_name = _('category')
        verbose_name_plural = _('categories')


class Image(CreateUpdate):
    """Products' images"""
    picture = models.ImageField(_('picture'), max_length=8192, upload_to=settings.IMAGES_DIR)

    def __str__(self):
        return self.picture.name

    class Meta(object):
        ordering = ['-created']
        verbose_name = _('image')
        verbose_name_plural = _('images')


class Product(CreateUpdate, ActiveState):
    """Products"""
    name = models.CharField(_('name'), max_length=255, db_index=True)
    category = models.ForeignKey(Category, verbose_name=_('category'))
    price = models.DecimalField(_('price'), decimal_places=8, max_digits=28)
    discount_rel = models.DecimalField(
        _('relative discount'),
        decimal_places=8,
        max_digits=28,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(1.0)]
    )
    discount_abs = models.DecimalField(
        _('absolute discount'),
        decimal_places=8,
        max_digits=28,
        default=0,
        validators=[MinValueValidator(0)]
    )
    images = models.ManyToManyField(Image, through='Gallery', blank=True)

    objects = models.Manager()
    objects_active = ActiveManager()

    def __str__(self):
        return self.name

    class Meta(object):
        ordering = ['name']
        verbose_name = _('product')
        verbose_name_plural = _('products')


class Gallery(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return '[{}]/[{}]'.format(self.product.name, self.image.picture.name)

    class Meta(object):
        ordering = ['product_id']
        verbose_name = _('gallery')
        verbose_name_plural = _('galleries')
