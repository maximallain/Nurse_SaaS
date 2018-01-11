from django.db import models
from datetime import date
from nurses_app.models.nurse import Nurse

class Visit(models.Model):
    date = models.DateField(default=date.today)
    time = models.TimeField(null = True)
    completed = models.BooleanField(default="False")
    #default duration visit is 2hours - MVP
    duration_visit = models.IntegerField(default=1800)
    soin = models.ForeignKey('patients_app.Soin', null=True)
    nurse = models.ForeignKey(Nurse, null=True)