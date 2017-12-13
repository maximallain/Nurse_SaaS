from django import forms
from datetime import date

class Soins(forms.Form):
    Treatment_Type_Choices = (
        ('SC', 'Soin courant'),
        ('SS', 'Soin Spécifique'),
        ('SID', 'Soin infirmier à domicile')
    )

    Treatment_Frequency_Choice = (
        ('1', 'Monday'),
        ('2', 'Tuesday'),
        ('3', 'Wednesday'),
        ('4', 'Thursday'),
        ('5', 'Friday'),
        ('6', 'Saturday'),
        ('7', 'Sunday')
    )

    nom_soin = forms.CharField(max_length=100, label= "Name")
    type_soin = forms.ChoiceField(choices=Treatment_Type_Choices, label="Type")
    frequence_soin = forms.MultipleChoiceField(choices=Treatment_Frequency_Choice, label="Frequency")
    strict_punctuality = forms.BooleanField(initial=False, label="Strict punctuality")
    start_date = forms.DateField(label="Start Date", widget=forms.DateInput(format='%d-%m-%Y'))
    treatment_duration = forms.IntegerField(max_value=180, min_value=0, label="Duration (days)")
