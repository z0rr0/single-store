# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-15 18:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedbacks', '0005_auto_20170413_2253'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('is_basic', models.BooleanField(default=False, help_text='basic template (can be only one for every assignment)', verbose_name='basic')),
                ('method', models.CharField(choices=[('text', 'plain text'), ('html', 'html'), ('multipart', 'multipart content')], db_index=True, default='text', max_length=32, verbose_name='method')),
                ('assignment', models.CharField(choices=[('request', 'request confirmation'), ('seller', 'seller notification')], db_index=True, default='request', max_length=32, verbose_name='assignment')),
                ('subject', models.CharField(max_length=255, verbose_name='subject')),
                ('body', models.TextField(blank=True, verbose_name='body')),
                ('body_html', models.TextField(blank=True, verbose_name='HTML body')),
            ],
            options={
                'verbose_name': 'email template',
                'verbose_name_plural': 'email templates',
                'ordering': ['name'],
            },
        ),
        migrations.AlterField(
            model_name='request',
            name='validation',
            field=models.CharField(choices=[('waiting', 'waiting'), ('confirmed', 'confirmed'), ('handled', 'rejected'), ('rejected', 'handled')], db_index=True, default='waiting', max_length=32, verbose_name='validation'),
        ),
    ]