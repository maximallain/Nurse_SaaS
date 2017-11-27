from django.conf.urls import url, include

from .views.accueil import accueil

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url('^accueil',accueil, name='accueil' )
]