# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-05 08:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0016_auto_20171004_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cut',
            name='updated_time',
            field=models.DateTimeField(verbose_name='תאריך'),
        ),
    ]
