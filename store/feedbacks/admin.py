# coding: utf-8

from django.contrib import admin

from .models import Request


class RequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'product', 'city', 'ip', 'comment', 'created')
    list_filter = ('created',)
    search_fields = ('name', 'phone', 'city')


admin.site.register(Request, RequestAdmin)
