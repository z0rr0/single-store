# coding: utf-8
import csv

from django.contrib import admin
from django.core import serializers
from django.http import HttpResponse

from feedbacks.models import Request, EmailTemplate


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'validation', 'phone', 'email', 'product', 'city', 'ip', 'comment', 'created')
    list_filter = ('created', 'validation')
    search_fields = ('name', 'phone', 'city')
    actions = ('export_as_json', 'export_as_csv')

    def export_as_json(self, request, queryset):
        response = HttpResponse(content_type='application/json')
        serializers.serialize('json', queryset, stream=response)
        return response

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="data.csv"'

        fieldnames = ['name', 'phone', 'created', 'email', 'city', 'validation', 'comment', 'internal_comment']
        writer = csv.DictWriter(response, fieldnames=fieldnames)
        writer.writeheader()
        for row in queryset.values(*fieldnames):
            writer.writerow(row)
        return response


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_basic', 'method', 'assignment', 'subject', 'modified')
    list_filter = ('method', 'assignment')
