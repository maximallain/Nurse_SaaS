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
        patient = context['patient']
        list_treatments = patient.treatments.all()
        list_dict = []
        for treatment in list_treatments :
            dict_treatment_date = {}
            list_dispo = list(map(lambda x: int(x), treatment.frequence_soin))
            days_treatment = []
            for int_day in list_dispo :
                for tuple in Soin.Treatment_Frequency_Choice :
                    if str(int_day) == tuple[0] :
                        days_treatment.append(tuple[1])
            dict_treatment_date['treatment'] = treatment
            dict_treatment_date['date']= days_treatment
            list_dict.append(dict_treatment_date)
        context['list_dict'] = list_dict
        return context

    def post(self, request, pk):
        if "Deletion Treatment" in request.POST:
            treatment_pk = request.POST.get("Deletion Treatment","")
            Soin.objects.filter(pk=treatment_pk)[0].delete()
            return HttpResponseRedirect(reverse("patient_detail", args=[pk]))

