from django.conf.urls import url, include
from .views.nurses import nurses

urlpatterns = [
    url('^', include('django.contrib.auth.urls')), 
    url('^nurses', nurses, name="nurses")
]