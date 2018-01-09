from django.shortcuts import render
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from infirmiers_app.models.nurse import Nurse
from soins_app.models.visits import Visit

@method_decorator(login_required, name='dispatch')
class NurseDetailView(DetailView):
    """This class is based on DetailView special feature in Django"""
    model = Nurse #This view is based on the model Nurse
    template_name = "nurse_detail.html" #The template linked to this ListView

    def get_context_data(self, **kwargs):
        context = super(NurseDetailView, self).get_context_data(**kwargs)
        print(context['nurse'].pk)
        list_visits = Visit.objects.filter(nurse = context['nurse'].pk)
        context['list_visits'] = list_visits
        return context