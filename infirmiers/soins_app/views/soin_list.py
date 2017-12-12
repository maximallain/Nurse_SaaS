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
        return HttpResponseRedirect(reverse("availability_creation_view", args=[soin_id])) #Redirect to the availability_creation_view
