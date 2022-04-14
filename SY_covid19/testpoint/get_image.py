# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : get_image.py
# Time       ：2022/4/13 23:30
# Author     ：Gao Shan
# Description：
"""
import requests
from bs4 import BeautifulSoup as bs
import os

print(os.getcwd())
os.chdir('./info2_image')
print(os.getcwd())

URL='https://new.qq.com/omn/20220413/20220413A0AQBF00.html'
response=requests.get(URL)
soup=bs(response.text,'lxml')
img_url=soup.find_all('img')
i=0
for url in img_url:
    img_url=url.get('src')
    print(img_url)
    response=requests.get('http:'+img_url)
    i+=1
    with open(str(i)+'.jpg','wb') as f:
        f.write(response.content)
