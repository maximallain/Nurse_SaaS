from django.shortcuts import render
from soins_app.forms.new_patients import Patients_Form
from soins_app.models.Patients import Patient
from django.http import HttpResponseRedirect
from django.urls import reverse
from signUp.models.office import Office

def patient_request(request):

    if request.method == 'POST':
        form = Patients_Form(request.POST)

        if form.is_valid():
            nom = form.cleaned_data['nom']
            prenom = form.cleaned_data['prenom']
            adresse = form.cleaned_data['adresse']
            telephone = form.cleaned_data['telephone']
            email = form.cleaned_data['email']
            office = Office.objects.filter(user = request.user )[0]

            #Check telephone can be converted to an integer
            try:
                int(telephone)
            except ValueError:
                error_message = "Le numéro de téléphone doit être sous format numérique"
                return render(request, 'nouveau_patient.html', {'form': form, 'error_message' : error_message})
    
            Patient(nom=nom, prenom = prenom, adresse = adresse, telephone = telephone,email=email,office=office).save()
            return HttpResponseRedirect(reverse("patient_list"))
    else:
        form = Patients_Form()

    return render(request, 'nouveau_patient.html', {'form' : form})
