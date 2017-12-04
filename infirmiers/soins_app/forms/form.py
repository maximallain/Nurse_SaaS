from django import forms


class Soins(forms.Form):
    nom_soin = forms.CharField(max_length=100)
    type_soin = forms.CharField(max_length=100)
    adresse_soin = forms.CharField(max_length=100)
    frequence_soin = forms.CharField(max_length=100)
    ponctualite_definie = forms.CharField(max_length=100)
