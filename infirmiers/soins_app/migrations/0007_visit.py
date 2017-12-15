# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-12 14:10
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('infirmiers_app', '0003_merge_20171209_0848'),
        ('soins_app', '0006_auto_20171212_1348'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('start_time', models.TimeField()),
                ('completed', models.BooleanField(default='False')),
                ('duration_visit', models.IntegerField(default=2)),
                ('nurse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='infirmiers_app.Nurse')),
            ],
        ),
    ]