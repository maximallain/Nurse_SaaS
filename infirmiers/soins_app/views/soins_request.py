from django.shortcuts import render
from soins_app.forms.new_soins import Soins
from soins_app.models.soins import Soin

def soins_request(request):
    """
    :param request:
    :return:
    """

    form = Soins(request.POST or None)

    if form.is_valid():
        nom_soin = form.cleaned_data['nom_soin']
        type_soin = form.cleaned_data['type_soin']
        adresse_soin = form.cleaned_data['adresse_soin']
        frequence_soin = form.cleaned_data['frequence_soin']
        ponctualite_definie = form.cleaned_data['ponctualite_definie']
        Soin(nom_soin=nom_soin, type_soin = type_soin, adresse_soin = adresse_soin, frequence_soin = frequence_soin, ponctualite_definie = ponctualite_definie).save()

    envoi=True

    return render(request, 'nouveau_soin.html', locals())