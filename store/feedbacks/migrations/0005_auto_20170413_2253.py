# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-13 19:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedbacks', '0004_remove_request_range'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='internal_comment',
            field=models.TextField(blank=True, verbose_name='internal comment'),
        ),
        migrations.AddField(
            model_name='request',
            name='validation',
            field=models.CharField(choices=[('waiting', 'waiting'), ('confirmed', 'confirmed'), ('handled', 'handled'), ('rejected', 'rejected')], db_index=True, default='waiting', max_length=32, verbose_name='validation'),
        ),
    ]
