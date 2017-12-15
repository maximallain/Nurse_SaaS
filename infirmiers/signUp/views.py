from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import SignUpForm, SignUpFormOffice
from .models.office import Office

def signup(request):
    if request.method == 'POST':
        user_form = SignUpForm(request.POST)
        office_form = SignUpFormOffice(request.POST)
        if user_form.is_valid() and office_form.is_valid():
            user_form.save()

            username = user_form.cleaned_data.get('username')
            user_current = User.objects.filter(username = username)[0]

            office_adress = office_form.cleaned_data['adress']
            office = Office(adress=office_adress, user = user_current)
            office.save()

            raw_password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        user_form = SignUpForm()
        office_form = SignUpFormOffice()
    return render(request, 'registration/signup.html', {'user_form': user_form, 'office_form' : office_form})