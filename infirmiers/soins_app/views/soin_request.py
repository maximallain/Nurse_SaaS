from soins_app.forms.new_soins import Soins
from soins_app.models.soins import Soin
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

def soin_request(request, patient_id):

    if request.method == 'POST':
        form = Soins(request.POST)

        if form.is_valid():
            nom_soin = form.cleaned_data['nom_soin']
            type_soin = form.cleaned_data['type_soin']
            frequence_soin = form.cleaned_data['frequence_soin']
            strict_punctuality = form.cleaned_data['strict_punctuality']
            start_date=form.cleaned_data['start_date']
            treatment_duration=form.cleaned_data['treatment_duration']
            #envoi = True
            Soin(nom_soin=nom_soin,
                 type_soin = type_soin,
                 frequence_soin = frequence_soin,
                 strict_punctuality = strict_punctuality,
                 start_date=start_date,
                 treatment_duration=treatment_duration,
                 patient_id=patient_id
                 ).save()
            #return HttpResponseRedirect(reverse("patient_detail"), {'patient_pk' : patient_id})
            return HttpResponseRedirect(reverse("patient_list"))

    else:
        form = Soins()

    return render(request, 'nouveau_soin.html', {'form': form, 'patient_pk': patient_id})

        #return render(request, 'nouveau_soin.html', {'form' : form, patient_pk:patient_pk})
