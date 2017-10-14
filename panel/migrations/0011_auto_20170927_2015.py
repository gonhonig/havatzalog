# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-27 17:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0010_auto_20170922_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parameter',
            name='category',
            field=models.CharField(choices=[('התנהלות מקצועית', 'התנהלות מקצועית'), ('חשיבה והצגה', 'חשיבה והצגה'), ('ערכים', 'ערכים'), ('פיקוד ומנהיגות', 'פיקוד ומנהיגות'), ('קבוצה ובין אישי', 'קבוצה ובין אישי'), ('יעדים', 'יעדים'), ('אחר', 'אחר')], max_length=250, verbose_name='קטגוריה'),
        ),
    ]
