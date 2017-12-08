from django import forms

class AvailabilityForm(forms.Form):

    WeekDay_Choices = (
        ('M', 'Monday'),
        ('T', 'Tuesday'),
        ('W', 'Wednesday'),
        ('Th', 'Thursday'),
        ('F', 'Friday'),
        ('S', 'Saturday'),
        ('Su', 'Sunday'),
    )

    AvailableDay = forms.MultipleChoiceField(label="Day", choices=WeekDay_Choices)
    Start_time = forms.TimeField(label="Start", widget=forms.TimeInput(format='%H:%M'))
    End_time = forms.TimeField(label="End", widget=forms.TimeInput(format='%H:%M'))