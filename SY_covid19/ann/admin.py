# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : admin.py
# Time       ：2022/4/1 0:07
# Author     ：Gao Shan
# Description：
"""
from django.contrib import admin
from .models import Article,Patient


class PatientInline(admin.StackedInline):
    model=Patient


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id','title','type','source','pub_date')
    list_filter = ('type','source','pub_date',"edit_date")
    search_fields = ('title','content',)
    date_hierarchy = "pub_date"
    ordering = ['-pub_date']
    inlines=(PatientInline,)

@admin.register(Patient)
class PatinetAdmin(admin.ModelAdmin):
    list_display = ['patient_id','address_now','article_related','pub_date']
    list_filter = ['address_now']
    ordering = ['-id']

    def patient_id(self,Patient):
        return '病例'+str(Patient.id)

    def pub_date(self,Patinet):
        return Patinet.article_related.pub_date
