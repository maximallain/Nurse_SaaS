from soins_app.forms.new_soins import Soins
from soins_app.models.soins import Soin
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

def soin_request(request):

    if request.method == 'POST':
        form = Soins(request.POST)

        if form.is_valid():
            nom_soin = form.cleaned_data['nom_soin']
            type_soin = form.cleaned_data['type_soin']
            adresse_soin = form.cleaned_data['adresse_soin']
            frequence_soin = form.cleaned_data['frequence_soin']
            ponctualite_definie = form.cleaned_data['ponctualite_definie']
            #envoi = True
            Soin(nom_soin=nom_soin, type_soin = type_soin, adresse_soin = adresse_soin, frequence_soin = frequence_soin, ponctualite_definie = ponctualite_definie).save()
            return HttpResponseRedirect(reverse("soin_list"))
    else:
        form = Soins()

    return render(request, 'nouveau_soin.html', {'form' : form})
