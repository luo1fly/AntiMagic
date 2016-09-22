#!/usr/bin/env python
# Name: rest_urls.py
# Time:9/20/16 3:08 PM
# Author:luo1fly

from django.conf.urls import (url, include)
from rest_framework import routers
from assets import rest_views
# import custom modules above

router = routers.DefaultRouter()
router.register(r'users', rest_views.UserViewSet)
router.register(r'asset', rest_views.AssetViewSet)
router.register(r'server', rest_views.ServerViewSet)
# router.register(r'asset_list', rest_views.asset_list)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^asset_list/$', rest_views.asset_list),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
