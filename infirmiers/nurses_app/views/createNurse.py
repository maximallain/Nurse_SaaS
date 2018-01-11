from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required

from nurses_app.forms.nurseCreationForm import NurseCreationForm
from nurses_app.models.nurse import Nurse
from nurses_app.models.interval import Interval
from signUp.models.office import Office

@login_required
def nurse_creation_view(request):
    if request.method == 'POST':
        form = NurseCreationForm(request.POST)
        
        if form.is_valid():
            FirstName = form.cleaned_data['FirstName'].capitalize()
            LastName = form.cleaned_data['LastName'].upper()
            Gender = form.cleaned_data['Gender'][0]
            PhoneNumber = form.cleaned_data['PhoneNumber']
            office = Office.objects.filter(user = request.user )[0]

            #Check PhoneNumber can be converted to an integer
            try:
                int(PhoneNumber)
            except ValueError:
                error_message = "Le numéro de téléphone doit être sous format numérique"
                return render(request, 'createNurse.html', {'form': form, 'error_message' : error_message}) 

            nurse = Nurse(FirstName=FirstName, LastName=LastName, Gender=Gender, PhoneNumber=PhoneNumber, office=office)
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
