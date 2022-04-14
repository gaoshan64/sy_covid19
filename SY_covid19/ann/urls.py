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
    path('',views.chart_test,name='chart_test'),
    path('notice',views.notice,name='notice'),
    path('new_patient',views.new_patient,name='new_patient'),
    path('others',views.others,name='others'),
    path('detial_page/<int:article_id>',views.article_detial,name='article_detial'),
    path('first_add',views.first_add,name='first_add'),
    path('get_new', views.get_new, name='first_add'),
    path('batch_add_patient', views.batch_add_patient, name='batch_add_patient'),
    path('chart_test/<str:range>',views.chart_test,name='chart_test'),
    #path('chart_test2',views.chart_test2,name='chart_test2')
]
