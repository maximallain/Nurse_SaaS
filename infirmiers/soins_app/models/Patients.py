from django.db import models

from .soins import Soin
from signUp.models.office import Office


class Patient(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=100)
    telephone = models.CharField(max_length=10)
    email = models.EmailField(max_length=254)
    office = models.ForeignKey(Office, on_delete=models.CASCADE, null=True)
    treatments = models.ManyToManyField(Soin)