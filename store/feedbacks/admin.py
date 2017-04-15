# coding: utf-8

from django.contrib import admin

from .models import Request, EmailTemplate


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'validation', 'phone', 'email', 'product', 'city', 'ip', 'comment', 'created')
    list_filter = ('created', 'validation')
    search_fields = ('name', 'phone', 'city')


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_basic', 'method', 'assignment', 'subject', 'modified')
    list_filter = ('method', 'assignment')


# admin.site.register(Request, RequestAdmin)
