from django.views.generic import DetailView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.template import loader

from patients_app.models.soins import Soin
from patients_app.models.Patients import Patient


@method_decorator(login_required, name='dispatch')
class SoinDetailView(DetailView):
    """This class is based on DetailView special feature in Django"""
    model = Soin #This view is based on the model Nurse
    template_name = "soin_detail.html" #The template linked to this ListView

    def get_context_data(self, **kwargs):
        context = super(SoinDetailView, self).get_context_data(**kwargs)
        return context

    def Soin_Detail(request, patient_pk, treatment_pk):
        patient = Patient.objects.filter(pk=patient_pk)[0]
        treatment = Soin.objects.filter(pk=treatment_pk)[0]
        context = {'treatment': treatment, 'patient': patient}
        template = loader.get_template("soin_detail.html")
        return HttpResponse(template.render(request=request, context=context))
