from django.conf.urls import url, include

from .views.accueil import accueil
<<<<<<< HEAD

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url('^accueil',accueil, name='accueil' )
=======
from .views.createNurse import nurse_creation_view
from .views.nurse_list import NurseListView
from .views.nurse_detail import NurseDetailView

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url('^accueil',accueil, name='accueil' ),
    url('^creation',nurse_creation_view, name="nurse_creation_view"),
    url('^nurses$', NurseListView.as_view(), name='nurse_list'),
    url('^nurse/(?P<pk>\d+)$', NurseDetailView.as_view(), name='nurse_detail')

>>>>>>> Added the detail view of a nurse
]