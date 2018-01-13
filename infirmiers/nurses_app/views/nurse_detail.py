from django.shortcuts import render
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from nurses_app.models.nurse import Nurse
from patients_app.models.visits import Visit
from patients_app.models.Patients import Patient
from datetime import date,timedelta


@method_decorator(login_required, name='dispatch')
class NurseDetailView(DetailView):
    """This class is based on DetailView special feature in Django"""
    model = Nurse #This view is based on the model Nurse
    template_name = "nurse_detail.html" #The template linked to this ListView

    def get_context_data(self, **kwargs):
        context = super(NurseDetailView, self).get_context_data(**kwargs)
        today = date.today()
        tomorrow = today + timedelta(days=1)
        list_visits_today = Visit.objects.filter(nurse = context['nurse'].pk,date=today).order_by('time')
        list_visits_tomorrow = Visit.objects.filter(nurse = context['nurse'].pk,date=tomorrow).order_by('time')

        list_patient_all = Patient.objects.all()

        context_today =[]
        i=0
        for visit in list_visits_today :
            dict_visit = {}
            dict_visit['visit']=visit
            i=i+1
            dict_visit['number_visit']=i
            treatment = visit.soin
            dict_visit['treatment']=treatment
            for patient in list_patient_all :
                list_treatment_of_this_patient = patient.treatments.all()
                if treatment in list_treatment_of_this_patient :
                    dict_visit['patient'] = patient
            context_today.append(dict_visit)

        context_tomorrow = []
        i = 0
        for visit in list_visits_tomorrow:
            dict_visit = {}
            dict_visit['visit'] = visit
            i = i + 1
            dict_visit['number_visit'] = i
            treatment = visit.soin
            dict_visit['treatment'] = treatment
            for patient in list_patient_all:
                list_treatment_of_this_patient = patient.treatments.all()
                if treatment in list_treatment_of_this_patient:
                    dict_visit['patient'] = patient
            context_tomorrow.append(dict_visit)

        context['list_all_today'] = context_today
        context['list_all_tomorrow'] = context_tomorrow

        return context