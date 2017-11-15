# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-10 09:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='area',
            field=models.CharField(blank=True, max_length=250, verbose_name='אזור'),
        ),
        migrations.AlterField(
            model_name='task',
            name='content',
            field=models.TextField(verbose_name='תוכן'),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateField(blank=True, verbose_name='דד-ליין'),
        ),
        migrations.AlterField(
            model_name='task',
            name='reminder',
            field=models.DateTimeField(blank=True, verbose_name='תזכורת'),
        ),
        migrations.AlterField(
            model_name='task',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, verbose_name='נוצר'),
        ),
    ]
