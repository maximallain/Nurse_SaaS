from django.db import models
from datetime import date
from soins_app.models.visits import Visit
from .Patients import Patient


class Soin(models.Model):
    Treatment_Type_Choices = (
        ('SC', 'Soin courant'),
        ('SS', 'Soin Spécifique'),
        ('SID', 'Soin infirmier à domicile')
    )

    Treatment_Frequency_Choice = (
        ('1', 'Monday'),
        ('2', 'Tuesday'),
        ('3', 'Wednesday'),
        ('4', 'Thursday'),
        ('5', 'Friday'),
        ('6', 'Saturday'),
        ('7', 'Sunday')
    )
    
    nom_soin = models.CharField(max_length=100)
    type_soin = models.CharField(max_length=2, choices=Treatment_Type_Choices)
    frequence_soin = models.CharField(max_length=2, choices=Treatment_Frequency_Choice)
    ponctualite_definie = models.CharField(max_length=100)
    strict_punctuality = models.BooleanField(default=False)
    start_date = models.DateField(default=date.today)
    treatment_duration = models.IntegerField(default=0)
    patient = models.ForeignKey(Patient, default=1)
