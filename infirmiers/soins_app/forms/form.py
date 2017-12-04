from django import forms


class Soins(forms.Form):
    nom_soin = models.CharField(max_length=100)
    type_soin = models.CharField(max_length=100)
    adresse_soin = models.CharField(max_length=100)
    frequence_soin = models.CharField(max_length=100)
    ponctualite_definie = models.CharField(max_length=100)
