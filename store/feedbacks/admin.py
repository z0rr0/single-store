# coding: utf-8
import csv

from django.contrib import admin
from django.core import serializers
from django.db import models
from django.http import HttpResponse, HttpRequest
from django.utils.translation import ugettext_lazy as _

from feedbacks.models import Request, EmailTemplate


def move_to_confirmed(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: models.QuerySet):
    queryset.update(validation=Request.VALIDATION_CONFIRMED)
    modeladmin.message_user(request, _('Objects were updated successfully'))


def move_to_handled(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: models.QuerySet):
    queryset.update(validation=Request.VALIDATION_HANDLED)
    modeladmin.message_user(request, _('Objects were updated successfully'))


def move_to_rejected(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: models.QuerySet):
    queryset.update(validation=Request.VALIDATION_REJECTED)
    modeladmin.message_user(request, _('Objects were updated successfully'))


request_states = dict(Request.VALIDATION_CHOICES)
move_to_confirmed.short_description = '{}: {}'.format(
    _('Go to state'), request_states.get(Request.VALIDATION_CONFIRMED)
)
move_to_handled.short_description = '{}: {}'.format(
    _('Go to state'), request_states.get(Request.VALIDATION_HANDLED)
)
move_to_rejected.short_description = '{}: {}'.format(
    _('Go to state'), request_states.get(Request.VALIDATION_REJECTED)
)


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'validation', 'phone', 'email', 'product', 'city', 'comment', 'created')
    list_filter = ('created', 'validation')
    search_fields = ('name', 'phone', 'city')
    actions = ('export_as_json', 'export_as_csv', move_to_confirmed, move_to_handled, move_to_rejected)

    def export_as_json(self, request: HttpRequest, queryset: models.QuerySet):
        response = HttpResponse(content_type='application/json')
        serializers.serialize('json', queryset, stream=response)
        return response

    def export_as_csv(self, request: HttpRequest, queryset: models.QuerySet):
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
