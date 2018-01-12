from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import SignUpForm, SignUpFormOffice
from .models.office import Office
import requests as req
from patients_app.views.patient_request import KEY

def signup(request):
    if request.method == 'POST':
        user_form = SignUpForm(request.POST)
        office_form = SignUpFormOffice(request.POST)
        if user_form.is_valid() and office_form.is_valid():
            office_adress = office_form.cleaned_data['adress']
            if not req.get("https://maps.googleapis.com/maps/api/distancematrix/json?origins=" +
                           office_adress.replace(" ", "%20") + "&destinations=" + office_adress.replace(" ", "%20")
                           + "&key=" + KEY).json().get("destination_addresses")[0] == "":

                user_form.save()

                username = user_form.cleaned_data.get('username')
                user_current = User.objects.filter(username = username)[0]

                office = Office(adress=office_adress, user = user_current)
                office.save()

                raw_password = user_form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                office_pk = Office.objects.filter(user = user)[0].pk
                return HttpResponseRedirect(reverse("home"))
            else:
                error_message = "Invalid address"
                return render(request, 'registration/signup.html', {'user_form': user_form, 'office_form' : office_form, 'error_message': error_message})
    else:
        user_form = SignUpForm()
        office_form = SignUpFormOffice()
    return render(request, 'registration/signup.html', {'user_form': user_form, 'office_form' : office_form})