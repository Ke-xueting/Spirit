# -*- coding: utf-8 -*-

from django.conf.urls import re_path

from ...core.conf import settings
from . import views


app_name = 'category'
urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^create/$', views.create, name='create'),
    re_path(r'^update/(?P<category_id>[0-9]+)/$', views.update, name='update'),

    re_path(r'^create_sub/$', views.create_sub, name='create_sub'),

]

if settings.ST_ORDERED_CATEGORIES:
    urlpatterns.extend([
        re_path(r'^move-up/(?P<category_id>[0-9]+)/$', views.move_up, name='move_up'),
        re_path(r'^move-dn/(?P<category_id>[0-9]+)/$', views.move_dn, name='move_dn')
    ])
