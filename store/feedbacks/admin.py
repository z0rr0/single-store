# coding: utf8

from django.contrib import admin

from .models import Request


class RequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'city', 'ip', 'created')
    list_filter = ('created',)
    search_fields = ('phone', 'city')


admin.site.register(Request, RequestAdmin)
