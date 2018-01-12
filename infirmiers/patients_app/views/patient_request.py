from django.shortcuts import render
from patients_app.forms.new_patients import Patients_Form
from patients_app.models.Patients import Patient
from django.http import HttpResponseRedirect
from django.urls import reverse
from signUp.models.office import Office
from django.contrib.auth.decorators import login_required
import requests as req

KEY = "AIzaSyATtwrFvepaVpvY0oYYyY_G71Mk97D7yzo"


@login_required
def patient_request(request):

    if request.method == 'POST':
        form = Patients_Form(request.POST)

        if form.is_valid():
            Address = form.cleaned_data['Address']
            if not req.get("https://maps.googleapis.com/maps/api/distancematrix/json?origins=" +
                           Address.replace(" ", "%20") + "&destinations=" + Address.replace(" ", "%20")
                           + "&key=" + KEY).json().get("destination_addresses")[0] == "":
                FirstName = form.cleaned_data['FirstName'].capitalize()
                LastName = form.cleaned_data['LastName'].upper()
                PhoneNumber = form.cleaned_data['PhoneNumber']
                Email = form.cleaned_data['Email']
                office = Office.objects.filter(user = request.user )[0]

                #Check telephone can be converted to an integer
                try:
                    int(PhoneNumber)
                except ValueError:
                    error_message = "The number must be numerical"
                    return render(request, 'nouveau_patient.html', {'form': form, 'error_message' : error_message})

                Patient(LastName = LastName, FirstName = FirstName, Address = Address, PhoneNumber = PhoneNumber,Email = Email,office = office).save()
                return HttpResponseRedirect(reverse("patient_list"))
            else:
                error_message = "Invalid address"
                return render(request, 'nouveau_patient.html', {'form': form, 'error_message': error_message})
    else:
        form = Patients_Form()

    return render(request, 'nouveau_patient.html', {'form' : form})
