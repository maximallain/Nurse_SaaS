from django.db import models
from nurses_app.models.interval import Interval
from signUp.models.office import Office

class Nurse(models.Model):
    Gender_Choices = (
        ('F', 'Female'),
        ('M', 'Male'),
    )
    intervals = models.ManyToManyField(Interval)
    FirstName = models.CharField(max_length=50)
    LastName = models.CharField(max_length=50)
    Gender = models.CharField(max_length=1, choices=Gender_Choices) 
    PhoneNumber = models.CharField(max_length=10, unique=True)
    office = models.ForeignKey(Office, on_delete=models.CASCADE, null=True)
    

    



