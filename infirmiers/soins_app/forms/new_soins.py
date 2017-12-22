from django import forms
from datetime import date

class Soins(forms.Form):
    Treatment_Type_Choices = (
        ('SC', 'Soin courant'),
        ('SS', 'Soin Spécifique'),
        ('SID', 'Soin infirmier à domicile')
    )

    Treatment_Frequency_Choice = (
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday')
    )

    nom_soin = forms.CharField(max_length=100, label= "Name")
    type_soin = forms.ChoiceField(choices=Treatment_Type_Choices, label="Type")
    frequence_soin = forms.MultipleChoiceField(choices=Treatment_Frequency_Choice, label="Frequency")
    strict_punctuality = forms.BooleanField(initial=False, label="Strict punctuality", required=False)
    start_date = forms.DateField(label="Start Date (format:YYYY-M-D)")
    treatment_duration = forms.IntegerField(max_value=180, min_value=0, label="Duration (days)")
