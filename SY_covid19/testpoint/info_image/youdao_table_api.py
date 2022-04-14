# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : youdao.py
# Time       ：2022/4/14 0:37
# Author     ：Gao Shan
# Description：
"""
# -*- coding: utf-8 -*-

import uuid
import requests
import base64
import hashlib
import time
import os
import json
from pprint import pprint
import base64




YOUDAO_URL = 'https://openapi.youdao.com/ocr_table'
APP_KEY = '4e1d6e0923c6b32d'
APP_SECRET = 'DpEi8tD54xb1LFsrNIxGEV6hf79gKaUJ'


def truncate(q):
    if q is None:
        return None
    q_utf8 = q.decode("utf-8")
    size = len(q_utf8)
    return q_utf8 if size <= 20 else q_utf8[0:10] + str(size) + q_utf8[size - 10:size]


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


def connect(path):
    f = open(path, 'rb')  # 二进制方式打开图文件
    q = base64.b64encode(f.read())  # 读取文件内容，转换为base64编码
    f.close()

    data = {}
    data['type'] = '1'
    data['q'] = q
    data['docType'] = 'excel'
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['salt'] = salt
    data['sign'] = sign

    response= do_request(data).json()
    return response

def excel_base64(path):
    response_json = connect(path)
    if response_json['errorCode'] == '0':
        return response_json['Result']['tables'][0]
    else:
        print (response_json['errorCode'])  # 打印错误码


def decode_base64(base64_str):
    base64_data = base64_str.encode('utf-8')
    origin_data = base64.b64decode(base64_data)
    return origin_data

def save_excel(base64_str, path='1.xlsx'):
    origin_data = decode_base64(base64_str)
    with open(path, 'wb') as f:
        f.write(origin_data)

def image_to_excel(path):
    base64_str = excel_base64(path)
    save_excel(base64_str)


if __name__ == '__main__':
    image_to_excel('10.png')