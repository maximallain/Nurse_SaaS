from django.shortcuts import render

def accueil(request):
    message_accueil = 5
    return render(request,'accueil.html',locals())
