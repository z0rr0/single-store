# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-12 22:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedbacks', '0003_auto_20170409_2127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='range',
        ),
    ]
