# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-16 17:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_specification'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='logo',
            field=models.ImageField(blank=True, max_length=8192, null=True, upload_to='product_images', verbose_name='logo'),
        ),
    ]
