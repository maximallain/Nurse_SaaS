"""infirmiers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from infirmiers import views as home_view
from infirmiers import admin_lte_views as a_lte




urlpatterns = [
    url(r'^$', home_view.home, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^infirmier/', include('infirmiers_app.urls')),
    url(r'^soins/', include('soins_app.urls')),
    url(r'^signup/', include('signUp.urls')),
    url(r'^api/v1/', include('api.urls')),
    url(r'bower_components/(?P<path>.*)$',a_lte.bower_view, name="bower_components"),
    url(r'dist/(?P<path>.*)$',a_lte.dist_view, name="dist"),

]
