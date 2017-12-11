from django.conf.urls import url, include

from .views.createNurse import nurse_creation_view
from .views.nurse_list import NurseListView
from .views.nurse_detail import NurseDetailView
from .views.create_availability import availability_creation_view

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url('^creation',nurse_creation_view, name="nurse_creation_view"),
    url('^nurses$', NurseListView.as_view(), name='nurse_list'),
    url('^nurses/(?P<nurse_id>\d+)', NurseListView.as_view(), name='nurse_list'),
    url('^nurse/(?P<pk>\d+)$', NurseDetailView.as_view(), name='nurse_detail'),
    url('^availability/(?P<nurse_id>\d+)$',availability_creation_view, name="availability_creation_view")

]