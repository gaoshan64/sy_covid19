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



def get_location_json_by_address(address_now='沈阳市大东区龙之梦畅园'):
    ak='I1vUfuxw5861emgW8TBkuzitM28bdZuP'
    url='https://api.map.baidu.com/place/v2/search?query={}' \
        '&region=沈阳' \
        '&citi_limit=true' \
        '&scope=1' \
        '&output=json' \
        '&ak={}'.format(address_now,ak)
    resp=requests.get(url).json()

    return resp



def d_c_l_get(str_now='沈阳市大东区龙之梦畅园'):
    '''
    通过地址描述查询 坐标经纬度 区 小区名称
    :param str_now:
    :return:
    '''
    result=get_location_json_by_address(str_now)
    if result['message']=='ok':
        lng=result['results'][0]['location']['lng']
        lat=result['results'][0]['location']['lat']
        try:
            district=result['results'][0]['area']
        except:
            district=result['results'][0]['address']
        comunity=result['results'][0]['name']
        return lng,lat,district,comunity
    else:
        print('查询失败')
        return None




if __name__ =='__main__':
    input=input('请输入地址：')
    pprint(d_c_l_get(input))