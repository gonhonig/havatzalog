# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-23 07:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0032_event_updated_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(verbose_name='תאריך'),
        ),
    ]