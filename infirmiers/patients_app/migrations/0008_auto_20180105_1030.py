# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-05 10:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patients_app', '0007_remove_soin_ponctualite_definie'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patient',
            old_name='adresse',
            new_name='Adress',
        ),
        migrations.RenameField(
            model_name='patient',
            old_name='email',
            new_name='Email',
        ),
        migrations.RenameField(
            model_name='patient',
            old_name='nom',
            new_name='FirstName',
        ),
        migrations.RenameField(
            model_name='patient',
            old_name='prenom',
            new_name='LastName',
        ),
        migrations.RenameField(
            model_name='patient',
            old_name='telephone',
            new_name='PhoneNumber',
        ),
    ]
