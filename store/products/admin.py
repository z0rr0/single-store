# coding: utf8

from django.contrib import admin

from .models import Category, Image, Product, Gallery


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'modified')
    list_filter = ('modified',)


class ImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'height', 'width', 'size', 'modified')
    list_filter = ('modified',)

    def name(self, obj):
        return obj.picture.name

    def size(self, obj):
        return obj.picture.size

    def height(self, obj):
        return obj.picture.height

    def width(self, obj):
        return obj.picture.width


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'discount_rel', 'discount_abs')
    list_filter = ('category', 'modified', 'created')


class GalleryAdmin(admin.ModelAdmin):
    list_display = ('image', 'product')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Gallery, GalleryAdmin)
