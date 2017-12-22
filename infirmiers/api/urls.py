from django.conf.urls import url, include
from .views.nurses_list import NursesList
from .views.visits_list import VisitList
from .views.nurse_detail import nurse_detail
from .views.visit_detail import visit_detail
from .views.visits_list_post import VisitsListPostAPIView

urlpatterns = [
    url('^', include('django.contrib.auth.urls')), 
    url('^nurses/(?P<officepk>[0-9]+)/$', NursesList.as_view(), name="nurses_office_list_api"),
    url('^nurses/$', NursesList.as_view(), name="nurses_office_list_api"),
    url('^nurse/(?P<pk>[0-9]+)/$', nurse_detail, name="nurse_detail_api"),
    url('^visits/create', VisitsListPostAPIView.as_view(), name="visits_list_api_create"),
    url('^visits/', VisitList.as_view(), name="visits_list_api"),
    url('^visit/(?P<pk>[0-9]+)/$', visit_detail, name="visit_detail_api"),
    
]