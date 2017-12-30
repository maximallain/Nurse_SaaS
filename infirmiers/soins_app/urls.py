from django.conf.urls import url, include

from .views.soin_request import soin_request
from .views.patient_request import patient_request
from .views.soin_detail import SoinDetailView
from .views.patient_list import PatientListView
from .views.patient_detail import PatientDetailView


urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url('^patients$', PatientListView.as_view(), name='patient_list'),
    url('^patients/(?P<id>\d+)', PatientListView.as_view(), name='patient_list'),
    url('^creation_soins/(?P<patient_id>\d+)', soin_request, name='soin_request'),
    #url('^creation_soins', soin_request, name='soin_request'),
    url('^creation_patient', patient_request, name='patient_request'),
    url('^soin/(?P<pk>\d+)$', SoinDetailView.as_view(), name='soin_detail'),
    url('^patient/(?P<pk>\d+)$', PatientDetailView.as_view(), name='patient_detail'),

    #url('^soin/(?P<soin_id>\d+)', SoinListView.as_view(), name='soin_list'),
    #url('^patient_detail', PatientDetailView, name='patient_detail'),
    # url('^soin_detail', patient_request, name='soin_detail'),
]
