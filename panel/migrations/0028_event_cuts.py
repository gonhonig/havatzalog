# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-19 23:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0027_remove_cut_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='cuts',
            field=models.ManyToManyField(to='panel.Cut', verbose_name='פרמטרים'),
        ),
    ]