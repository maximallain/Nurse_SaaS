from django.conf.urls import url, include

from .views.soin_detail import SoinDetailView
from .views.soin_request import soin_request
from .views.patient_request import patient_request
from .views.patient_list import PatientListView
from .views.patient_detail import PatientDetailView

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url('^patients$', PatientListView.as_view(), name='patient_list'),
    url('^patients/(?P<id>\d+)', PatientListView.as_view(), name='patient_list'),
    url('^creation_soins/(?P<patient_id>\d+)', soin_request, name='soin_request'),
    url('^creation_patient', patient_request, name='patient_request'),
    url('^patient/(?P<pk>\d+)$', PatientDetailView.as_view(), name='patient_detail'),
    url('^soin/(?P<patient_pk>\d+)/(?P<treatment_pk>\d+)$', SoinDetailView.Soin_Detail, name='soin_detail'),

]
