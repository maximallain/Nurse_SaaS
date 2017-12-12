from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView

from soins_app.models.soins import Soin

class SoinListView(ListView):
    """This class is based on ListView special feature in Django"""
    model = Soin #This view is based on the model Nurse
    template_name = "soins_list.html" #The template linked to this ListView

    def get_context_data(self, **kwargs):
        context = super(SoinListView, self).get_context_data(**kwargs)
        return context


    def post(self, request, soin_id):
        if "Deletion" in request.POST:
            Soin.objects.filter(pk=soin_id)[0].delete()
            return HttpResponseRedirect(reverse("soin_list"))
        """elif "NewForm" in request.POST:
            return HttpResponseRedirect(reverse("patient_detail",args=[patient_id]))"""

