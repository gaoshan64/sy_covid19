# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : admin.py
# Time       ：2022/4/1 0:07
# Author     ：Gao Shan
# Description：
"""
from django.contrib import admin
from .models import Article,Patient,Community
from django.utils.html import format_html
from django.urls import reverse


def linkify(field_name):
    """
    Converts a foreign key value into clickable links.

    If field_name is 'parent', link text will be str(obj.parent)
    Link will be admin url for the admin url for obj.parent.id:change
    """

    def _linkify(obj):
        linked_obj = getattr(obj, field_name)
        if linked_obj is None:
            return '-'
        app_label = linked_obj._meta.app_label
        model_name = linked_obj._meta.model_name
        view_name = f'admin:{app_label}_{model_name}_change'
        link_url = reverse(view_name, args=[linked_obj.pk])
        return format_html('<a href="{}">{}</a>', link_url, linked_obj)

    _linkify.short_description = field_name  # Sets column name
    return _linkify


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
    list_display = ['patient_id','address_now','district',linkify('article_related'),'definite_date','pub_date']
    list_filter = ['address_now','district','definite_date']
    ordering = ['-id']

    def patient_id(self,Patient):
        return '病例'+str(Patient.id)

    def pub_date(self,Patinet):
        return Patinet.article_related.pub_date

@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ['name','district','lng','lat']
    list_filter = ['district']