from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from signUp.models.office import Office
import requests

@login_required
def home(request):

    if request.method == 'POST':
        user = request.user
        officepk = Office.objects.filter(user = user)[0].pk
        requests.get("http://127.0.0.1:5000/optimize?officepk=" + str(officepk))

    current_user_id = request.user
    current_office = Office.objects.filter(user = request.user)[0]
    return render(request, 'home.html', locals())

def starter(request):
    return render(request, 'starter.html')