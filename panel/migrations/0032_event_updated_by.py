# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-21 23:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('panel', '0031_auto_20171020_0228'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='updated_by',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='עודכן על ידי'),
        ),
    ]
