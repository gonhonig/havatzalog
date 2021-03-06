# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-15 20:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0008_auto_20171114_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='content_type',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
        migrations.AlterField(
            model_name='task',
            name='object_id',
            field=models.PositiveIntegerField(blank=True),
        ),
    ]
