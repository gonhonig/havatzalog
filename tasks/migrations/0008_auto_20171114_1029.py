# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-14 08:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_auto_20171113_1612'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['deadline']},
        ),
    ]
