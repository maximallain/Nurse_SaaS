from django.db import models
from infirmiers_app.models.interval import Interval

class Nurse(models.Model):
    Gender_Choices = (
        ('F', 'Female'),
        ('M', 'Male'),
    )
    intervals = models.ManyToManyField(Interval)
    FirstName = models.CharField(max_length=50)
    LastName = models.CharField(max_length=50)
    Gender = models.CharField(max_length=1, choices=Gender_Choices) 
    PhoneNumber = models.IntegerField(unique=True)
    Office = models.IntegerField()
    

    



