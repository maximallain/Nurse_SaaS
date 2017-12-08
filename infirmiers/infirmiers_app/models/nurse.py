from django.db import models
from infirmiers_app.models.availableDay import AvailableDay

class Nurse(models.Model):
    Gender_Choices = (
        ('F', 'Female'),
        ('M', 'Male'),
    )
    availableDays = models.ManyToManyField(AvailableDay)
    FirstName = models.CharField(max_length=50)
    LastName = models.CharField(max_length=50)
    Gender = models.CharField(max_length=1, choices=Gender_Choices) 
    PhoneNumber = models.IntegerField()
    Office = models.IntegerField()
    

    



