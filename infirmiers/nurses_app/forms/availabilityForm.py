from django import forms

class AvailabilityForm(forms.Form):

    WeekDay_Choices = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )

    AvailableDay = forms.MultipleChoiceField(label="Day", choices=WeekDay_Choices)
    Start_time = forms.TimeField(label="Start (format-HH:MM)", widget=forms.TimeInput(format='%H:%M'))
    End_time = forms.TimeField(label="End (format-HH:MM)", widget=forms.TimeInput(format='%H:%M'))