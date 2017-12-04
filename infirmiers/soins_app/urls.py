from django.conf.urls import url, include

from .views.views import soins

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url('^creation_soins',soins, name='soins' )
]