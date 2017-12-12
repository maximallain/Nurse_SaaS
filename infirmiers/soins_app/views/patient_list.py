from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView

from soins_app.models.Patients import Patient

class PatientListView(ListView):
    """This class is based on ListView special feature in Django"""
    model = Patient #This view is based on the model Nurse
    template_name = "patient_list.html" #The template linked to this ListView

    def get_context_data(self, **kwargs):
        context = super(PatientListView, self).get_context_data(**kwargs)
        return context

    def post(self, request, patient_id):
        if "Deletion" in request.POST:
            Patient.objects.filter(pk=patient_id)[0].delete()
            return HttpResponseRedirect(reverse("patient_list"))