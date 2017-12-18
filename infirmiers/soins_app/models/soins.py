from django.db import models
from datetime import *
from .visits import Visit
from multiselectfield import MultiSelectField

class Soin(models.Model):
    Treatment_Type_Choices = (
        ('SC', 'Soin courant'),
        ('SS', 'Soin Spécifique'),
        ('SID', 'Soin infirmier à domicile')
    )

    Treatment_Frequency_Choice = (
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday')
    )

    nom_soin = models.CharField(max_length=100)
    type_soin = models.CharField(max_length=2, choices=Treatment_Type_Choices)
    ponctualite_definie = models.CharField(max_length=100)
    strict_punctuality = models.BooleanField(default=False)
    start_date = models.DateField(default=date.today)
    treatment_duration = models.IntegerField(default=0)
    #patient = models.IntegerField(default=0)
    frequence_soin = MultiSelectField(max_length=2, choices=Treatment_Frequency_Choice)


    #Autogeneration of visits in database when saving a care
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
    #retourne sous forme de liste d'entiers
    liste_dispo = list(map(lambda x: int(x), soin.frequence_soin))
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