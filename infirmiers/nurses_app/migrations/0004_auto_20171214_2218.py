# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-14 22:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nurses_app', '0003_merge_20171209_0848'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='availableday',
            name='intervals',
        ),
        migrations.RemoveField(
            model_name='nurse',
            name='availableDays',
        ),
        migrations.AddField(
            model_name='interval',
            name='weekday',
            field=models.CharField(choices=[('M', 'Monday'), ('T', 'Tuesday'), ('W', 'Wednesday'), ('Th', 'Thursday'), ('F', 'Friday'), ('S', 'Saturday'), ('Su', 'Sunday')], max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='nurse',
            name='intervals',
            field=models.ManyToManyField(to='nurses_app.Interval'),
        ),
        migrations.AlterUniqueTogether(
            name='interval',
            unique_together=set([('start_time', 'end_time', 'weekday')]),
        ),
        migrations.DeleteModel(
            name='AvailableDay',
        ),
    ]
