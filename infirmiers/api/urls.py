from django.conf.urls import url, include
from .views.nurses_list import nurses_list
from .views.visits_list import visits_list
from .views.nurse_detail import nurse_detail
from .views.visit_detail import visit_detail

urlpatterns = [
    url('^', include('django.contrib.auth.urls')), 
    url('^nurses', nurses_list, name="nurses_list"),
    url('^nurse/(?P<pk>[0-9]+)/$', nurse_detail, name="nurse_detail"),
    url('^visits', visits_list, name="visits_list"),
    url('^visit/(?P<pk>[0-9]+)/$', visit_detail, name="visit_detail")
]