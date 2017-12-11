from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView

from infirmiers_app.models.nurse import Nurse

class NurseListView(ListView):
    """This class is based on ListView special feature in Django"""
    model = Nurse #This view is based on the model Nurse
    template_name = "nurse_list.html" #The template linked to this ListView

    def get_context_data(self, **kwargs):
        context = super(NurseListView, self).get_context_data(**kwargs)
        return context

    def post(self, request, nurse_id):
        if "NewForm" in request.POST:
            return HttpResponseRedirect(reverse("availability_creation_view", args=[nurse_id])) #Redirect to the availability_creation_view
        elif "Deletion" in request.POST:
            Nurse.objects.filter(pk = nurse_id)[0].delete()
            return HttpResponseRedirect(reverse("nurse_list"))
