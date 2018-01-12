from django.db import models

from .soins import Soin
from signUp.models.office import Office


class Patient(models.Model):
    LastName = models.CharField(max_length=100)
    FirstName = models.CharField(max_length=100)
    Address = models.CharField(max_length=100)
    PhoneNumber = models.CharField(max_length=10)
    Email = models.EmailField(max_length=254)
    office = models.ForeignKey(Office, on_delete=models.CASCADE, null=True)
    treatments = models.ManyToManyField(Soin)