from django.shortcuts import render
from django.views.generic import DetailView
from soins_app.models.Patients import Patient

class PatientDetailView(DetailView):
    """This class is based on DetailView special feature in Django"""
    model = Patient #This view is based on the model Nurse
    template_name = "patient_detail.html" #The template linked to this ListView

    def get_context_data(self, **kwargs):
        context = super(PatientDetailView, self).get_context_data(**kwargs)
        return context