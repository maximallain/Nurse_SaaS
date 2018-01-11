from django.shortcuts import render
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from nurses_app.models.nurse import Nurse
from patients_app.models.visits import Visit
from patients_app.models.Patients import Patient


@method_decorator(login_required, name='dispatch')
class NurseDetailView(DetailView):
    """This class is based on DetailView special feature in Django"""
    model = Nurse #This view is based on the model Nurse
    template_name = "nurse_detail.html" #The template linked to this ListView

    def get_context_data(self, **kwargs):
        context = super(NurseDetailView, self).get_context_data(**kwargs)
        list_visits = Visit.objects.filter(nurse = context['nurse'].pk).order_by('time')
        list_patient_all = Patient.objects.all()
        context_final =[]
        i=0
        for visit in list_visits :
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
            context_final.append(dict_visit)
        context['list_visits'] = list_visits
        context['list_all'] = context_final
        return context