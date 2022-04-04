# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : form.py
# Time       ：2022/4/1 13:13
# Author     ：Gao Shan
# Description：
"""
from django import forms

from .models import Article,Patient

class ArticleForm(forms.ModelForm):

    class Meta:
        model=Article
        exclude=()

class PatientForm(forms.ModelForm):
    class Meta:
        model=Patient
        exclude=()
