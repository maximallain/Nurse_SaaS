from django.shortcuts import render
from soins_app.forms.new_patients import Patients_Form
from soins_app.models.Patients import Patient
from django.http import HttpResponseRedirect
from django.urls import reverse
from signUp.models.office import Office
from django.contrib.auth.decorators import login_required

@login_required
def patient_request(request):

    if request.method == 'POST':
        form = Patients_Form(request.POST)

        if form.is_valid():
            LastName = form.cleaned_data['LastName'].upper()
            FirstName = form.cleaned_data['FirstName'].capitalize()
            Adress = form.cleaned_data['Adress']
            PhoneNumber = form.cleaned_data['PhoneNumber']
            Email = form.cleaned_data['Email']
            office = Office.objects.filter(user = request.user )[0]

            #Check telephone can be converted to an integer
            try:
                int(PhoneNumber)
            except ValueError:
                error_message = "The number must be numerical"
                return render(request, 'nouveau_patient.html', {'form': form, 'error_message' : error_message})
    
            Patient(LastName = LastName, FirstName = FirstName, Adress = Adress, PhoneNumber = PhoneNumber,Email = Email,office = office).save()
            return HttpResponseRedirect(reverse("patient_list"))
    else:
        form = Patients_Form()

    return render(request, 'nouveau_patient.html', {'form' : form})
