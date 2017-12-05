from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from infirmiers_app.forms.nurseCreationForm import NurseCreationForm
from infirmiers_app.models.nurse import Nurse
from infirmiers_app.models.availableDay import AvailableDay
from infirmiers_app.models.interval import Interval

def nurse_creation_view(request):
    if request.method == 'POST':
        form = NurseCreationForm(request.POST)
        if form.is_valid():
            FirstName = form.cleaned_data['FirstName']
            LastName = form.cleaned_data['LastName']
            Gender = form.cleaned_data['Gender'][0]
            PhoneNumber = form.cleaned_data['PhoneNumber']

            nurse = Nurse(FirstName=FirstName, LastName=LastName, Gender=Gender, PhoneNumber=PhoneNumber)
            nurse.save()

            return HttpResponseRedirect(reverse("nurse_list"))

    else:
        form = NurseCreationForm()

    return render(request, 'createNurse.html', {'form': form})
