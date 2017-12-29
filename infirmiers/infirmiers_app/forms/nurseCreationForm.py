from django import forms

class NurseCreationForm(forms.Form):
    Gender_Choices = (
        ('F', 'Female'),
        ('M', 'Male'),
    )

    FirstName = forms.CharField(label="First Name", max_length=50)
    LastName = forms.CharField(label="Last Name", max_length=50)
    Gender = forms.MultipleChoiceField(label="Gender", choices=Gender_Choices) 
    PhoneNumber = forms.CharField(label="Phone Number", min_length=10, max_length=10)