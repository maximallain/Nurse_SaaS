# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-22 15:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soins_app', '0004_visit_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='duration_visit',
            field=models.IntegerField(default=1800),
        ),
    ]
