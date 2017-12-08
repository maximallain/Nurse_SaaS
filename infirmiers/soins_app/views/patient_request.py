from django.shortcuts import render
from soins_app.forms.new_patients import Patients_Form
from soins_app.models.patients import Patients

def soins_request(request):
    """
    :param request:
    :return:
    """

    form = Patients_Form(request.POST or None)

    if form.is_valid():
        nom = form.cleaned_data['nom']
        prenom = form.cleaned_data['prénom']
        adresse = form.cleaned_data['adresse']
        telephone = form.cleaned_data['téléphone']
        email = form.cleaned_data['email']

        Patients(nom=nom, prenom = prenom, adresse = adresse, telephone = telephone,email=email).save()

    envoi=True

    return render(request, 'nouveau_patient.html', locals())