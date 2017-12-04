from django.shortcuts import render
from soins_app.forms.form import Soins

def soins(request):
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

    envoi=True

    return render(request, 'nouveau_soin.html', locals())