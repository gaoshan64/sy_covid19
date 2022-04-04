# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : urls.py.py
# Time       ：2022/3/31 23:10
# Author     ：Gao Shan
# Description：
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello_world,name='index'),
    path('notice',views.notice,name='notice'),
    path('new_patient',views.new_patient,name='new_patient'),
    path('others',views.others,name='others'),

    path('first_add',views.first_add,name='first_add'),
    path('get_new', views.get_new, name='first_add'),
]
