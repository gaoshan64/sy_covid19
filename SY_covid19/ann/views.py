# Create your views here.

from django.shortcuts import HttpResponse,render,get_object_or_404
from .op_api import *
import json
from .spyder import Spider
from .models import Article,Patient,Community
from  .form import ArticleForm
from .extract import extract_data,p_definite_date
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from pyecharts import options as opts
from pyecharts.charts import Bar,Line
import datetime
from django.db.models import Count
from pyecharts.globals import ThemeType
from .get_baidu_data import get_baidu_v_data


def hello_world(request):
    '''
    首页
    :param request:
    :return:
    '''
    articles = Article.objects.all()
    paginator = Paginator(articles, 20)
    page = request.GET.get('page')
    title='沈阳Covid-19'
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
    return render(request,'./base.html',{"articles":articles,"page":current_page,"title":title})


def notice(request):
    '''

    :param request:
    :return:
    '''
    articles = Article.objects.filter(type='ann')
    title='通知通告'
    paginator = Paginator(articles, 20)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
    return render(request,'./base.html',{"articles":articles,"page":current_page,"title":title})



def new_patient(request):
    '''

    :param request:
    :return:
    '''
    articles = Article.objects.filter(type='new_p')
    paginator = Paginator(articles, 20)
    page = request.GET.get('page')
    title="确诊病例"
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
    return render(request,'./base.html',{"articles":articles,"page":current_page,"title":title})



def others(request):
    '''

    :param request:
    :return:
    '''

    articles = Article.objects.filter(type='alert')
    title='其他'
    paginator = Paginator(articles, 20)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
    return render(request, './base.html', {"articles": articles, "page": current_page,"title":title })



def article_detial(request,article_id):
    '''
    文章详情
    :param request:
    :param article_id:
    :return:
    '''

    article=get_object_or_404(Article,id=article_id)
    return render(request,'./detial.html',{"article":article})


def time_range_choice(timerange='y'):
    '''
    获取时间范围
    :param timerange:
    :return:
    '''

    now_time = datetime.datetime.now()
    day_num = now_time.isoweekday()
    monday =(now_time-datetime.timedelta(days=day_num))
    if timerange == 'w':
        p_datas = Patient.objects.filter(definite_date__range=(monday, now_time))
        print('#',now_time,monday)
    elif timerange == 'm':
        p_datas=Patient.objects.filter(definite_date__month=now_time.month)
    else:
        p_datas = Patient.objects.filter(definite_date__year=now_time.year)

    return p_datas


def get_dis_bar(range='y'):
    p_datas=time_range_choice(range)
    district_set = p_datas.values('district')
    district_count_set = district_set.annotate(number=Count('district'))
    dis_list = [(x['district'], x['number']) for x in district_count_set]

    def takeSecond(elem):
        return elem[1]

    dis_list.sort(key=takeSecond)
    # 按照数量多少排序
    return dis_list


def get_d_c_bar(range):
    dis_list=get_dis_bar(range)#获取区 病例数量列表
    dis_list=[x[0] for x in dis_list] #获取区名称列表 按数量由少到多排序
    community_d_list=get_com_bar(range)
    community_d_list2=[[x[0],dis_list.index(x[1]),x[2] ]for x in community_d_list]
    #print(community_d_list2)
    def getlist(a,b):
        list=[0]*len(dis_list)
        list[a]=b
        return list

    community_d_list3=[[x[0],getlist(x[1],x[2])]for x in community_d_list2]

    return community_d_list3

def get_com_bar(range='y'):
    #get a list of community and its count
    p_datas=time_range_choice(range)    #获取时间范围
    community_set = p_datas.values('community','district') #
    community_count_set = community_set.annotate(number=Count('community'))
    print (community_count_set)
    com_list = [(x['community'], x['district'], x['number']) for x in community_count_set]
    #com_name=Community.objects.get(id=270).name
    def get_name(id):
        return Community.objects.get(id=id).name
    com_list2=[(get_name(x[0]),x[1],x[2]) for x in  com_list]

    #print(com_name)
    return com_list2

def chart_test(request,range='y'):
    ##### 关于柱状图
    data_d=get_dis_bar(range)
    # 获取X 轴 经过排序的 区

    x_d=[x[0] for x in data_d]
    y_d=[y[1] for y in data_d ]
    # 获取Y 轴
    data_dc=get_d_c_bar(range)

    #y_d=[y[1] for y in data_d]
    title='数据分析'
    d=(
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(x_d)
        #.add_yaxis("各区确诊病例数量", y_d)
        .add_yaxis('总数',y_d,color='white',label_opts=opts.LabelOpts(is_show=True))


    )
    for x in data_dc:

        d.add_yaxis(x[0],x[1],stack="stack")
    d.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    d.set_global_opts(
        title_opts=opts.TitleOpts(title="各区确诊病例数量", subtitle=""),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-60)),
        legend_opts=opts.LegendOpts(type_='scroll',pos_left='10%',pos_right='20%',pos_top='10%')

    )
    data_bar=d.dump_options()
    #c.render()
    #print(chart)
    # data_c=get_com_bar(range)
    # x_c = [x[0] for x in data_c]
    # y_c = [y[1] for y in data_c]
    # c = (
    #     Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    #         .add_xaxis(x_c)
    #         .add_yaxis("各小区确诊病例数量", y_c)
    #
    #         .set_global_opts(title_opts=opts.TitleOpts(title="各小区确诊病例数量", subtitle=""),
    #                          xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-60,is_show=False)))
    # )
    # community = c.dump_options()


    # 关于地图标记点
    c_d_list=get_com_bar(range)
    #print (c_d_list)
    points_list = []
    for x in c_d_list:
        point_dict={'name':x[0],'number':x[2],'di':x[1]}
        point_location_dict=get_lng_lat(x[0])

        print(point_dict,point_location_dict)
        point_dict.update(point_location_dict)
        #print(point_dict)
        points_list.append(point_dict)

    # points = [
    #     {"lng": 123.492272, "lat": 41.805323, "number": 1, "name": "龙之梦畅园", "di": "大东区"},
    # ]
    # [('东惠民家园', '大东区', 1), ('东望街海狮公寓', '大东区', 1), ('东陶路后堡东巷', '大东区', 1), ('中体奥林匹克花园新城', '大东区', 5), ('前谟村', '苏家屯区', 1),
    #  ('华瑞家园', '浑南区', 3), ('城中花园小区', '和平区', 1), ('塔湾街向阳北小区', '皇姑区', 1), ('宁山中路亚洲城小区', '皇姑区', 1),
    #  ('宜必思酒店（沈阳北站南广场店）', '沈河区', 2), ('客车司机', '铁西区', 1), ('富力尚悦居', '大东区', 2), ('崇山中路公务员小区', '皇姑区', 1),
    #  ('年丰园小区', '于洪区', 1), ('延河街延河小区', '皇姑区', 1), ('建赏欧洲小区', '皇姑区', 3), ('惠民家园', '大东区', 5), ('望花新村小区', '大东区', 1),
    #  ('沈铁民族佳园', '和平区', 1), ('沙河子小区', '于洪区', 3),


    points=json.dumps(points_list)

    #print(points)
    #####关于 曲线图
    three_list=get_baidu_v_data()
    data_list, patient_list, positive_list=three_list
    now_time = datetime.datetime.now()
    day_num = now_time.isoweekday()
    monday = (now_time - datetime.timedelta(days=day_num)).timetuple()
    monday_str="{}.{}".format(monday.tm_mon,monday.tm_mday)

    month=now_time.month
    month_first_day_str='{}.1'.format(str(month))

    month_first_day_index=data_list.index(month_first_day_str)
    monday_index=data_list.index(monday_str)
    print('monday_index:',monday_index)
    print('month_first_day_index:',month_first_day_index)
    print(data_list[monday_index-len(data_list):])
    if range == 'w':
        data_list_r=data_list[monday_index-len(data_list):]
        patient_list=patient_list[monday_index-len(data_list):]
        positive_list=positive_list[monday_index-len(data_list):]
    elif range == 'm':
        data_list_r=data_list[month_first_day_index-len(data_list):]
        patient_list = patient_list[month_first_day_index - len(data_list):]
        positive_list = positive_list[month_first_day_index - len(data_list):]
    else:
        data_list_r=data_list

    l=(
        Line(init_opts=opts.InitOpts(theme=ThemeType.ROMA))
        .add_xaxis(data_list_r)
        .add_yaxis('本地确诊病例',patient_list,is_smooth=True,
                   linestyle_opts=opts.LineStyleOpts(width=2))
        .add_yaxis('无症状感染者',positive_list,is_smooth=True,
                   linestyle_opts=opts.LineStyleOpts(width=2))
        .set_global_opts(
            title_opts=opts.TitleOpts(title='感染日期曲线',subtitle=''),
        )
        )

    data_line=l.dump_options()



    return render(request,'./chart.html',{'data_bar':data_bar,'data_line':data_line,'title':title,'points':points})





def chart_test2(request):
    return render(request,'chart2.html')






