from django.db import models


class Patient(models.Model):
    nom = models.CharField(max_length=100, default="")
    prenom = models.CharField(max_length=100, default="")
    adresse = models.CharField(max_length=100, default="")
    telephone = models.CharField(max_length=10, default="")
    email = models.EmailField(default="")
