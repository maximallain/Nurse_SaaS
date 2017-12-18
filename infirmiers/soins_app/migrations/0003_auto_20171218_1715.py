# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-18 17:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('signUp', '0002_auto_20171215_1533'),
        ('soins_app', '0002_remove_soin_patient'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='Office',
        ),
        migrations.AddField(
            model_name='patient',
            name='office',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='signUp.Office'),
        ),
    ]
