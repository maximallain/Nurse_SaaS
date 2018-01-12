from django.views.generic import DetailView
from patients_app.models.Patients import Patient
from patients_app.models.soins import Soin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class PatientDetailView(DetailView):
    """This class is based on DetailView special feature in Django"""
    model = Patient #This view is based on the model Nurse
    template_name = "patient_detail.html" #The template linked to this ListView

    def get_context_data(self, **kwargs):
        context = super(PatientDetailView, self).get_context_data(**kwargs)
        conversion_dict_treatment_type=dict(Soin.Treatment_Type_Choices)
        print(conversion_dict_treatment_type)
        return context

    def post(self, request,patient_id):
        if "Deletion Treatment" in request.POST:
            treatment_pk = request.POST.get("Deletion Treatment","")
            Soin.objects.filter(pk=treatment_pk)[0].delete()
            return HttpResponseRedirect(reverse("patient_detail", args=[patient_id]))

