from django import forms
from datetime import date

class Soins(forms.Form):
    Treatment_Type_Choices = (
        ('CT', 'Common treatment'),
        ('ST', 'Specific Treatment'),
        ('ET', 'Exceptional Treatment')
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

    name_soin = forms.CharField(max_length=100, label= "Name")
    type_soin = forms.ChoiceField(choices=Treatment_Type_Choices, label="Type")
    frequence_soin = forms.MultipleChoiceField(choices=Treatment_Frequency_Choice, label="Frequency", widget=forms.CheckboxSelectMultiple)
    start_date = forms.DateField(label="Start Date (format:YYYY-MM-DD)")
    treatment_duration = forms.IntegerField(max_value=180, min_value=0, label="Duration (days)")
    specific_visit_time = forms.TimeField(label="Start time (format-HH:MM)", widget=forms.TimeInput(format='%H:%M'), required=False)