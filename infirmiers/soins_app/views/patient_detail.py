from django.views.generic import DetailView
from soins_app.models.Patients import Patient
from django.http import HttpResponseRedirect
from django.urls import reverse

class PatientDetailView(DetailView):
    """This class is based on DetailView special feature in Django"""
    model = Patient #This view is based on the model Nurse
    template_name = "patient_detail.html" #The template linked to this ListView

    def get_context_data(self, **kwargs):
        context = super(PatientDetailView, self).get_context_data(**kwargs)
        return context

    def post(self, request, patient_id):
        if "Deletion" in request.POST:
            Patient.objects.filter(pk=patient_id)[0].delete()
            return HttpResponseRedirect(reverse("patient_list"))
        """elif "NewForm" in request.POST:
            return HttpResponseRedirect(reverse("patient_detail", args=[patient_id]))"""
