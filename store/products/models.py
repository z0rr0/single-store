# coding: utf-8
from decimal import Decimal

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from libs.models import CreateUpdate, ActiveState, ActiveManager


class Category(CreateUpdate):
    """Product categories"""
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    logo = models.ImageField(_('logo'), max_length=8192, upload_to=settings.IMAGES_DIR, blank=True, null=True)

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
        ordering = ['pk']
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
    description = models.TextField(_('description'), blank=True)
    specification = models.TextField(_('specification'), blank=True)

    objects = models.Manager()
    objects_active = ActiveManager()

    def __str__(self):
        return self.name

    class Meta(object):
        ordering = ['name']
        verbose_name = _('product')
        verbose_name_plural = _('products')

    @property
    def final_discount(self) -> Decimal:
        return self.price * self.discount_rel + self.discount_abs

    @property
    def final_price(self) -> Decimal:
        return self.price - self.final_discount

    @cached_property
    def one_image(self) -> Image:
        return self.images.first()

    @cached_property
    def tail_images(self) -> models.QuerySet:
        return self.images.all()[1:]

    @property
    def short_description(self) -> str:
        if self.description:
            return self.description.split('\n')[0]
        return ''


class Gallery(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return '[{}]/[{}]'.format(self.product.name, self.image.picture.name)

    class Meta(object):
        ordering = ['product_id']
        verbose_name = _('gallery')
        verbose_name_plural = _('galleries')
