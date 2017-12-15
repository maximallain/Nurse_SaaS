# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-12 13:48
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soins_app', '0004_auto_20171212_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='soin',
            name='start_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='soin',
            name='strict_punctuality',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='soin',
            name='treatment_duration',
            field=models.IntegerField(default=0),
        ),
    ]