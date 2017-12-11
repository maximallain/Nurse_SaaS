from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from signUp import views as signUp_views


urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', signUp_views.signup, name='signup'),
]