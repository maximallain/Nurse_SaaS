# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-13 16:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('soins_app', '0009_soin_patient'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='visit',
            name='start_time',
        ),
    ]
