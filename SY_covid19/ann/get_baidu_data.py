# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : get_baidu_data.py
# Time       ：2022/4/8 21:18
# Author     ：Gao Shan
# Description：
"""
import requests
from pprint import pprint
import re
import json


def get_baidu_v_data():
    cookies = {
        'BAIDUID': '1CB0F8B5D9F8BEEFF2C8C451F0884BB6:FG=1',
        'BAIDUID_BFESS': '1CB0F8B5D9F8BEEF17CDF56FE4DFEAE4:FG=1',
        'BDUSS': 'lFRY2J2bDM5NkJFMlVBTX5DWXBrblJZczJ-NTJDZkVRcDRIZVduRWlOZnlkblppRVFBQUFBJCQAAAAAAAAAAAEAAABgFU0JdWlkX2JsYWNrc21pdGgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPLpTmLy6U5iY',
        'BDUSS_BFESS': 'lFRY2J2bDM5NkJFMlVBTX5DWXBrblJZczJ-NTJDZkVRcDRIZVduRWlOZnlkblppRVFBQUFBJCQAAAAAAAAAAAEAAABgFU0JdWlkX2JsYWNrc21pdGgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPLpTmLy6U5iY',
        'MCITY': '-%3A',
        'ZD_ENTRY': 'bing',
        'ab_sr': '1.0.1_OTY4MjQ1M2E1NTY1M2FlM2E5MjI5NTkwZWQwMDg0NGNjZDJiODhhMzlkYTFkY2JkZWU4YzcyYmMzZGMxZDNjZTgwOGY0ZTRjNzNmMDkzNmY4YzNlZWZlZGVhMWViNjNlNjBiYzRmMTcwOGM4NDU5OTFmMmJjZTg5ZGQ3MzkxYTdiNzg1MzM4ZjYxNzVmOWNlZWZjYWVhOTA2ZmU2ZDcwOA==',
        'lscaptain': 'srcactivitycaptainindexcss_91e010cf-srccommonlibsesljs_e3d2f596-srcactivitycaptainindexjs_a2e9c712',
        'Hm_lvt_68bd357b1731c0f15d8dbfef8c216d15': '1649423357',
        'Hm_lpvt_68bd357b1731c0f15d8dbfef8c216d15': '1649423357',
    }

    headers = {
        'authority': 'voice.baidu.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-dest': 'script',
        'referer': 'https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_aladin_banner&city=%E8%BE%BD%E5%AE%81-%E6%B2%88%E9%98%B3',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'BAIDUID=1CB0F8B5D9F8BEEFF2C8C451F0884BB6:FG=1; BAIDUID_BFESS=1CB0F8B5D9F8BEEF17CDF56FE4DFEAE4:FG=1; BDUSS=lFRY2J2bDM5NkJFMlVBTX5DWXBrblJZczJ-NTJDZkVRcDRIZVduRWlOZnlkblppRVFBQUFBJCQAAAAAAAAAAAEAAABgFU0JdWlkX2JsYWNrc21pdGgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPLpTmLy6U5iY; BDUSS_BFESS=lFRY2J2bDM5NkJFMlVBTX5DWXBrblJZczJ-NTJDZkVRcDRIZVduRWlOZnlkblppRVFBQUFBJCQAAAAAAAAAAAEAAABgFU0JdWlkX2JsYWNrc21pdGgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPLpTmLy6U5iY; MCITY=-%3A; ZD_ENTRY=bing; ab_sr=1.0.1_OTY4MjQ1M2E1NTY1M2FlM2E5MjI5NTkwZWQwMDg0NGNjZDJiODhhMzlkYTFkY2JkZWU4YzcyYmMzZGMxZDNjZTgwOGY0ZTRjNzNmMDkzNmY4YzNlZWZlZGVhMWViNjNlNjBiYzRmMTcwOGM4NDU5OTFmMmJjZTg5ZGQ3MzkxYTdiNzg1MzM4ZjYxNzVmOWNlZWZjYWVhOTA2ZmU2ZDcwOA==; lscaptain=srcactivitycaptainindexcss_91e010cf-srccommonlibsesljs_e3d2f596-srcactivitycaptainindexjs_a2e9c712; Hm_lvt_68bd357b1731c0f15d8dbfef8c216d15=1649423357; Hm_lpvt_68bd357b1731c0f15d8dbfef8c216d15=1649423357',
    }

    params = {
        'from': 'mola-virus',
        'stage': 'publish',
        'target': 'trendCity',
        'area': '\u8FBD\u5B81-\u6C88\u9633',
        'callback': 'jsonp_1649423429215_8931',
    }

    response_text = requests.get('https://voice.baidu.com/newpneumonia/getv2', headers=headers, params=params, cookies=cookies).text
    result_str=response_text[len(re.findall(r'jsonp_[\d_]+',response_text)[0])+1:-2]
    result_json=json.loads(result_str)
    data_list=result_json['data'][0]['trend']['updateDate']
    patient_list=result_json['data'][0]['trend']['list'][1]['data']
    positive_list=result_json['data'][0]['trend']['list'][0]['data']
    return data_list,patient_list,positive_list

if __name__ == '__main__':
    three_list=get_baidu_v_data()
    print(three_list[0])
    print(three_list[1])
    print(three_list[2])