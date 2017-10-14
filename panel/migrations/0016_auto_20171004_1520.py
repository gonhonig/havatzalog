# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-04 12:20
from __future__ import unicode_literals

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0015_auto_20171004_1126'),
    ]

    operations = [
        migrations.AddField(
            model_name='cut',
            name='headline',
            field=models.CharField(blank=True, max_length=40, verbose_name='כותרת'),
        ),
        migrations.AlterField(
            model_name='cut',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='תגיות'),
        ),
    ]
