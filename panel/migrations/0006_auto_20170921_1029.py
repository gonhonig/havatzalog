# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-21 07:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0005_auto_20170920_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cut',
            name='updated_time',
            field=models.DateTimeField(),
        ),
    ]
