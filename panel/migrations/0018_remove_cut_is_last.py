# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-05 12:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0017_auto_20171005_1114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cut',
            name='is_last',
        ),
    ]
