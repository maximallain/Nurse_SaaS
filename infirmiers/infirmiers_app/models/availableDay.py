from django.db import models

from infirmiers_app.models.interval import Interval

class AvailableDay(models.Model):
    WeekDay_Choices = (
        ('M', 'Monday'),
        ('T', 'Tuesday'),
        ('W', 'Wednesday'),
        ('Th', 'Thursday'),
        ('F', 'Friday'),
        ('S', 'Saturday'),
        ('Su', 'Sunday'),
    )
    
    intervals = models.ManyToManyField(Interval)
    weekday = models.CharField(max_length=2, choices=WeekDay_Choices)


    

    