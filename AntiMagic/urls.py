"""AntiMagic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
# from AntiMagic import views
from hosts import views as hosts_views
from hosts import urls as hosts_urls
from assets import urls as assets_urls
from assets import rest_urls

urlpatterns = [
    url(r'^$', hosts_views.index, name='dashboard'),
    url(r'^admin/', admin.site.urls),
    url(r'^asset/', include(assets_urls)),
    url(r'^hosts/', include(hosts_urls)),
    url(r'^logout/$', hosts_views.acc_logout, name='logout'),
    url(r'^api/', include(rest_urls)),
    url(r'^login/$', hosts_views.acc_login, name='login'),
    url(r'^monitor/$', hosts_views.monitor_index, name='monitor'),
]
