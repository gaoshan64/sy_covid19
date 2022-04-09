# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : spyder_sina.py
# Time       ：2022/4/5 10:40
# Author     ：Gao Shan
# Description：
"""


import requests
from pprint import pprint

URL='https://interface.sina.cn/news/wap/fymap2020_data.d.json'
URL_BAIDU='https://voice.baidu.com/act/newpneumonia/newpneumonia?city=%E8%BE%BD%E5%AE%81-%E6%B2%88%E9%98%B3'
URL_163='https://c.m.163.com/ug/api/wuhan/app/data/list-total'
respone=requests.get(URL_BAIDU).json()
pprint(respone)