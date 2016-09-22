#!/usr/bin/env python
# Name: urls.py
# Time:8/8/16 8:56 PM
# Author:luo1fly

from django.conf.urls import url
from hosts import views

urlpatterns = [
    url(r'^$', views.hosts_index, name='hosts'),
    url(r'^host_mgr/$', views.host_mgr, name='host_mgr'),
    url(r'^multi_cmd/$', views.multi_cmd, name='multi_cmd'),
    url(r'^submit_task/$', views.submit_task, name='submit_task'),
    url(r'^get_task_result/$', views.get_task_result, name='get_task_result'),
    url(r'^file_delivery/$', views.file_delivery, name='file_delivery'),
    url(r'^file_upload/$', views.file_upload, name='file_upload'),
]
