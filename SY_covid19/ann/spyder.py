# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : test1.py
# Time       ：2022/3/31 16:33
# Author     ：Gao Shan
# Description：
"""
import requests
from bs4 import BeautifulSoup as BS
import re


class Spider():

    def __init__(self):

        self.URL1 = 'http://www.shenyang.gov.cn/zt/fkxxgzbdgrdfyyq/tzgg/'
        self.headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer': 'http://www.shenyang.gov.cn/zt/fkxxgzbdgrdfyyq/tzgg/',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            # Requests sorts cookies= alphabetically
            'Cookie': 'zh_choose=s; zh_choose=s; _gscu_983269554=48711361ykm4mf17; _gscbrs_983269554=1; zh_choose=s; _trs_uv=l1eo6cdr_5451_5tu5; _trs_ua_s_1=l1eo6cdr_5451_1e1t; _gscs_983269554=48711361dmwq0g17|pv:42',
        }
        self.infor_list = []
        self.temp_html_doc = ""

    def get_list_page(self, page=1):
        # 采集第几页，如果第一页什么都不加，其他加入index路径
        if page == 1:
            page_str = ''
        else:
            page_str = 'index_{}.html'.format(str(page-1))
        URL = self.URL1 + page_str

        response = requests.get(URL, headers=self.headers, verify=False)
        html = response.content
        html_doc = str(html, 'utf-8')  # 解决编码问题
        # with open('list.html','w',encoding='utf-8') as f:
        #     f.write(html_doc)
        self.temp_html_doc = html_doc
        return html_doc

    def soup_list_page(self, page=1):
        html_doc = self.get_list_page(page)
        bs = BS(html_doc, 'lxml')
        list_ul = bs.find('ul', class_='xsy_rul1')  # 定位包含数据得ul标签
        a_list = list_ul.find_all('a')  # 定位所有a 标签
        # [(标题,链接，发布时间），.......]
        result_list = [[a.text.replace("\n", "").strip(),
                        self.URL1 + a.get('href')[2:],
                        a.nextSibling.nextSibling.text] for a in a_list]
        return result_list

    # 获取多页列表数据

    def more_list_page_data(self, page_number):
        result_list = []
        i = 1
        while i < page_number + 1:
            ind_pageinfor = self.soup_list_page(i)
            result_list.extend(ind_pageinfor)
            i += 1
        # 去重复
        # org_list=result_list
        # # no_du_list=list(set(org_list))
        # # no_du_list.sort(key=org_list.index)
        # # result_list=no_du_list
        self.infor_list = result_list
        return result_list

    def get_type(self, title):
        if title[0:2] == '新增':
            return 'new_p'
        elif title == '紧急健康提醒':
            return 'alert'
        else:
            return 'ann'

    # def infor_classify(self):
    #     w_list=self.soup_list_page()
    #     new_p_list=[]
    #     ann_list=[]
    #     for x in w_list:
    #         if x[0][0:2] == '新增':
    #             new_p_list.append(x)
    #             x.append('new_p')
    #         else:
    #             x.append('ann')
    #             ann_list.append(x)
    #     return {'ann':ann_list,'new_p':new_p_list}

    def get_detial_page(self, url):
        response = requests.get(url, headers=self.headers, verify=False)
        html = response.content
        html_doc = str(html, 'utf-8')  # 解决编码问题
        # with open('detial.html', 'w', encoding='utf-8') as f:
        #     f.write(html_doc)
        return html_doc

    def soup_detial_page(self, url):
        html_doc = self.get_detial_page(url)
        bs = BS(html_doc, 'lxml')
        infor_div = bs.find('div', class_='xsy_rcontent2')  #
        source = infor_div.find('div', class_='lysj').find_all('span')[1].text
        con_div= infor_div.find('div', class_='dlist_con content').div
        con_div=str(con_div)
        con=re.sub(pattern=r'<(\S*?)[^>]*>.*?|<.*? />',repl='\\n',string=con_div)
        con=re.sub(r'\u3000+|\n+',repl='\\n',string=con)
        con = re.sub(r'\u3000+|\n+', repl='\\n', string=con)
        return source,con


if __name__ == '__main__':
    gaoshan = Spider()
    result = gaoshan.more_list_page_data(1)

    print(result)
    one_detial = gaoshan.soup_detial_page(result[1][1])
    print(one_detial)
