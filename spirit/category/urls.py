# -*- coding: utf-8 -*-

from django.conf.urls import re_path

from . import views


app_name = 'category'
urlpatterns = [
    re_path(r'^$', views.index, name='index'),

    re_path(r'^(?P<pk>[0-9]+)/$', views.detail, kwargs={'slug': "", }, name='detail'),
    re_path(r'^(?P<pk>[0-9]+)/(?P<slug>[\w-]+)/$', views.detail, name='detail'),
]
