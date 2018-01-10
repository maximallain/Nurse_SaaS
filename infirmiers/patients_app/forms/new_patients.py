from django import forms


class Patients_Form(forms.Form):
    FirstName = forms.CharField(label="First Name", max_length=100)
    LastName = forms.CharField(label="Last Name", max_length=100)
    Adress = forms.CharField(label="Adress", max_length=100)
    PhoneNumber = forms.CharField(label="Phone Number", min_length=10, max_length=10)
    Email = forms.EmailField()
