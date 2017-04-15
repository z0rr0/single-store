# coding: utf-8

from django.contrib import admin

from .models import Category, Image, Product, Gallery
from libs.utils import round_money


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'modified')
    list_filter = ('modified',)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'height', 'width', 'size', 'modified')
    list_filter = ('modified',)

    def name(self, obj: Image):
        return obj.picture.name

    def size(self, obj: Image):
        return obj.picture.size

    def height(self, obj: Image):
        return obj.picture.height

    def width(self, obj):
        return obj.picture.width


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'discount_rel', 'discount_abs', 'final_price')
    list_filter = ('category', 'modified', 'created')
    search_fields = ('name',)

    def final_price(self, obj: Product):
        return round_money(obj.final_price)


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('image', 'product')
