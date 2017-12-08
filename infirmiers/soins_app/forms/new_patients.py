from django import forms


class Patients_Form(forms.Form):
    nom = forms.CharField(max_length=100)
    prenom = forms.CharField(max_length=100)
    adresse = forms.CharField(max_length=100)
    telephone = forms.CharField(max_length=10)
    email=forms.EmailField()