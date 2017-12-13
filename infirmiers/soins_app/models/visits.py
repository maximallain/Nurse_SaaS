from django.db import models
from datetime import date
from infirmiers_app.models.nurse import Nurse

class Visit(models.Model):
    date = models.DateField(default=date.today)
    start_time = models.TimeField()
    completed = models.BooleanField(default="False")
    #default duration visit is 2hours - MVP
    duration_visit = models.IntegerField(default=2)
    soin = models.ForeignKey('soins_app.Soin', default=1)
    nurse = models.ForeignKey(Nurse)