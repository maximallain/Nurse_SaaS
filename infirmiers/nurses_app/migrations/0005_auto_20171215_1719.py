# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-15 17:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('signUp', '0002_auto_20171215_1533'),
        ('nurses_app', '0004_auto_20171214_2218'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nurse',
            name='Office',
        ),
        migrations.AddField(
            model_name='nurse',
            name='office',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='signUp.Office'),
        ),
    ]
