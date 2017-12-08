from django.conf.urls import url, include

from .views.soins_request import soins_request
from .views.patient_request import patient_request

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url('^creation_soins', soins_request, name='soins_request'),
    url('^creation_patient', patient_request, name='patient_request')
]
