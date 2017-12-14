from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.utils import IntegrityError

from infirmiers_app.forms.nurseCreationForm import NurseCreationForm
from infirmiers_app.models.nurse import Nurse
from infirmiers_app.models.interval import Interval

def nurse_creation_view(request):
    if request.method == 'POST':
        form = NurseCreationForm(request.POST)
        
        if form.is_valid():
            FirstName = form.cleaned_data['FirstName']
            LastName = form.cleaned_data['LastName']
            Gender = form.cleaned_data['Gender'][0]
            PhoneNumber = form.cleaned_data['PhoneNumber']
            Office = request.user.id

            nurse = Nurse(FirstName=FirstName, LastName=LastName, Gender=Gender, PhoneNumber=PhoneNumber, Office=Office)
            try:
                nurse.save()
                return HttpResponseRedirect(reverse("nurse_list"))
            #Avoid the duplications of same nurse in database based on mobilephone
            except IntegrityError:
                form = NurseCreationForm()
                error_message = "Le numéro de téléphone est déjà utilisé pour un autre infirmier. Veuillez rentrer un autre numéro de téléphone"

                return render(request, 'createNurse.html', {'form': form, 'error_message' : error_message})  
        
        else:
            return render(request, 'index.html')


    else:
        form = NurseCreationForm()

    return render(request, 'createNurse.html', {'form': form})
