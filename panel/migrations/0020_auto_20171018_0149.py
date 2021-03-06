# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-17 22:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0019_auto_20171007_1455'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(max_length=40, verbose_name='כותרת')),
                ('details', models.TextField(verbose_name='פירוט')),
                ('date', models.DateTimeField(verbose_name='תאריך')),
            ],
        ),
        migrations.AlterField(
            model_name='cut',
            name='parameter',
            field=models.ManyToManyField(to='panel.Parameter', verbose_name='פרמטרים'),
        ),
        migrations.AddField(
            model_name='event',
            name='cuts',
            field=models.ManyToManyField(to='panel.Cut', verbose_name='פרמטרים'),
        ),
        migrations.AddField(
            model_name='event',
            name='pupil',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='panel.Pupil', verbose_name='חניך'),
        ),
    ]
