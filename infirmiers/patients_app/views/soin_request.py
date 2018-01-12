from patients_app.forms.new_soins import Soins
from patients_app.models.soins import Soin
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from patients_app.models.Patients import Patient
from django.contrib.auth.decorators import login_required
import datetime

@login_required
def soin_request(request, patient_id):

    if request.method == 'POST':
        form = Soins(request.POST)

        if form.is_valid():
            start_date=form.cleaned_data['start_date']
            try:
                if start_date > datetime.date.today():
                    name_soin = form.cleaned_data['name_soin']
                    type_soin = form.cleaned_data['type_soin']
                    frequence_soin = form.cleaned_data['frequence_soin']
                    specific_visit_time = form.cleaned_data['specific_visit_time']
                    treatment_duration=form.cleaned_data['treatment_duration']

                    soin =  Soin(name_soin=name_soin,
                         type_soin = type_soin,
                         frequence_soin = frequence_soin,
                         specific_visit_time = specific_visit_time,
                         start_date=start_date,
                         treatment_duration=treatment_duration,
                         patient = patient_id
                         )
                    soin.save()

                    patient = Patient.objects.get(pk = patient_id)
                    patient.treatments.add(soin)

                    return HttpResponseRedirect(reverse("patient_detail", args=[patient_id]))
                else:
                    return render(request, 'nouveau_soin.html', {'error_message' : "Invalid date", 'form': form, 'patient_pk': patient_id})
            except ValueError:
                return render(request, 'nouveau_soin.html',
                              {'error_message': "Invalid date", 'form': form, 'patient_pk': patient_id})
    else:
        form = Soins()

    return render(request, 'nouveau_soin.html', {'form': form, 'patient_pk': patient_id})

