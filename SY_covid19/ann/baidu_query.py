# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : baidu_query.py
# Time       ：2022/4/8 12:28
# Author     ：Gao Shan
# Description：
"""
import requests
from pprint import pprint

def get_location(address_now='沈阳市大东区龙之梦畅园'):
    ak='I1vUfuxw5861emgW8TBkuzitM28bdZuP'
    url='https://api.map.baidu.com/place/v2/search?query={}' \
        '&region=沈阳' \
        '&citi_limit=true' \
        '&scope=1' \
        '&output=json' \
        '&ak={}'.format(address_now,ak)
    resp=requests.get(url).json()
    result=resp['results'][0]['location']
    return result


if __name__ =='__main__':
    while True:
        address=input('input_address:')
        if address:
            resp=get_location(address)
        else:
            resp=get_location()
        pprint(resp)
