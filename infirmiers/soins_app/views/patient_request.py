from django.shortcuts import render
from soins_app.forms.new_patients import Patients_Form
from soins_app.models.patients import Patient

def patient_request(request):
    """
    :param request:
    :return:
    """

    form = Patients_Form(request.POST or None)

    if form.is_valid():
        nom = form.cleaned_data['nom']
        prenom = form.cleaned_data['prenom']
        adresse = form.cleaned_data['adresse']
        telephone = form.cleaned_data['telephone']
        email = form.cleaned_data['email']

        Patient(nom=nom, prenom = prenom, adresse = adresse, telephone = telephone,email=email).save()

    envoi=True

    return render(request, 'nouveau_patient.html', locals())