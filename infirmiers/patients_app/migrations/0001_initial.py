# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-18 15:08
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('nurses_app', '0004_auto_20171214_2218'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('adresse', models.CharField(max_length=100)),
                ('telephone', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('Office', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Soin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_soin', models.CharField(max_length=100)),
                ('type_soin', models.CharField(choices=[('SC', 'Soin courant'), ('SS', 'Soin Spécifique'), ('SID', 'Soin infirmier à domicile')], max_length=2)),
                ('ponctualite_definie', models.CharField(max_length=100)),
                ('strict_punctuality', models.BooleanField(default=False)),
                ('start_date', models.DateField(default=datetime.date.today)),
                ('treatment_duration', models.IntegerField(default=0)),
                ('patient', models.IntegerField(default=0)),
                ('frequence_soin', multiselectfield.db.fields.MultiSelectField(choices=[('0', 'Monday'), ('1', 'Tuesday'), ('2', 'Wednesday'), ('3', 'Thursday'), ('4', 'Friday'), ('5', 'Saturday'), ('6', 'Sunday')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('completed', models.BooleanField(default='False')),
                ('duration_visit', models.IntegerField(default=2)),
                ('nurse', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='nurses_app.Nurse')),
                ('soin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patients_app.Soin')),
            ],
        ),
        migrations.AddField(
            model_name='patient',
            name='treatments',
            field=models.ManyToManyField(to='patients_app.Soin'),
        ),
    ]
