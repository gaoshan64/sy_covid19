# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : op_api.py
# Time       ：2022/4/11 17:52
# Author     ：Gao Shan
# Description：
"""
from .views import *
from .form import *
from .models import *
from .baidu_query import d_c_l_get
from .extract import extract_data,p_definite_date
from .spyder import Spider

def batch_add(infor_list_t_l_d):
    '''
    批量添加 文章
    :param infor_list_t_l_d:
    :return:
    '''
    spr = Spider()
    for infor in  infor_list_t_l_d:
        try:
            new_article_detial=spr.soup_detial_page(infor[1])
        except Exception as e:
            print(e)
            print(infor)
            continue
        new_article_form=ArticleForm(
            data={'title':infor[0],'url':infor[1],'pub_date':infor[2],
                  'type':spr.get_type(infor[0]),
                  'source':new_article_detial[0],
                  'content':new_article_detial[1]}
        )
        if new_article_form.is_valid():
            cd =new_article_form.cleaned_data
            try:
                new_article = new_article_form.save()
                print(new_article,'#',new_article.id,'#',new_article.type)
                # if new_article.type=='new_p':
                #     patient_add(new_article)
            except Exception as e:
                print(e)
                continue
        else:
            print(new_article_form.errors)
            continue



def first_add(request):
    '''
    第一次添加文章
    :param request:
    :return:
    '''
    spr=Spider()
    infor_list_t_l_d=spr.more_list_page_data(4)
    #print(infor_list_t_l_d)

    batch_add(infor_list_t_l_d)
    return HttpResponse('finish')


def get_new(request):
    '''
    获取新文章
    :param request:
    :return:
    '''
    spr=Spider()
    page_1_list=spr.soup_list_page(1)

    new_article_list=[]
    for infor in page_1_list:
        a=Article.objects.filter(url=infor[1])
        if a.exists():
            print(infor[0],'not a new article')
            continue
        else:
            print(infor[0],'!!!!!!!',infor[0],'is a new article !!!!!!')
            new_article_list.append(infor)

    batch_add(new_article_list)
    return HttpResponse('finish')

def batch_add_patient(request):
    '''
    批量添加病人
    :param request:
    :return:
    '''
    article_list=Article.objects.filter(type='new_p')
    for article in article_list:
        patient_add(article)
    return HttpResponse('finish')

def patient_add(a_artical):
    '''

    :param a_artical:
    :return:
    '''
    content=a_artical.content
    definte_date=p_definite_date(content)

    patient_address_list=extract_data(a_artical.content)
    if a_artical.about_patient.all().count()==0:
        for address in patient_address_list:
            address_infor=d_c_l_get(address)
            if address_infor:
                com_instance=add_communiry(address_infor)
                lng, lat, district, comunity = address_infor

                new_patinet=Patient(address_now=address,
                                    article_related_id=a_artical.id,
                                    district=district,
                                    community=com_instance,
                                    definite_date=definte_date)
                new_patinet.save()
                print('New patient added !!!!!', new_patinet, address_infor)
            else:
                print('no address',a_artical.title)
                continue

    elif len(patient_address_list) == a_artical.about_patient.all().count():
        print('The patinets of this Article was added')

def add_communiry(address_infor):
    '''
    添加社区
    :param address_infor:
    :return:
    '''
    lng,lat,district,comunity=address_infor
    if Community.objects.filter(lng=lng,lat=lat).exists():
        print('Community already exist')
    else:
        new_community=Community(name=comunity,district=district,lng=lng,lat=lat)
        new_community.save()
        print('New community added',new_community)
    return Community.objects.filter(lng=lng,lat=lat)[0]

def get_lng_lat(address):
    '''
    获取经纬度
    :param address:
    :return:
    '''
    lng,lat=None,None
    try:
        address_instance=Community.objects.get(name=address)
        lng,lat=address_instance.lng,address_instance.lat

    except Exception as e:
        print(e)
        return None,None

    point_location_dict = {'lng': lng, 'lat': lat}
    #print(point_location_dict)
    return point_location_dict