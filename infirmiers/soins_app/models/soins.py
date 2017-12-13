from django.db import models
from datetime import *
from .visits import Visit
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
    patient = models.ForeignKey(Patient, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method.
        liste_visits = create_visits_from_soin(self)
        for date_visit in liste_visits:
            A = Visit()
            A.date = date_visit
            A.save()
            A.soin = self

def create_visits_from_soin(soin):
    i = 1
    visits = []
    current_date = soin.start_date
    #liste_dispo = list(map(lambda x: int(x), soin.frequence_soin))
    liste_dispo=[1,3,6] #en attente du format de choicefields
    current_index = liste_dispo.index(current_date.weekday())
    visits.append(soin.start_date)
    while i < soin.treatment_duration:
        try:
            next_weekday = liste_dispo[current_index + 1]
            timedeltadays = next_weekday - current_date.weekday()
        except IndexError:
            next_weekday = liste_dispo[0]
            timedeltadays = next_weekday + (7 - current_date.weekday())
        
        current_date += timedelta(days=timedeltadays)
        current_index = liste_dispo.index(current_date.weekday())

        visits.append(current_date)

        i = i + 1
    return visits