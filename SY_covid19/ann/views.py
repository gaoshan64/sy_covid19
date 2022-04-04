# Create your views here.


from django.shortcuts import HttpResponse,render
from django.db.models import Count

from .spyder import Spider
from .models import Article,Patient
from  .form import ArticleForm
from .extract import extract_data

def hello_world(request):
    return render(request,'./base.html')

def bath_add(infor_list_t_l_d):
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
                if new_article.type=='new_p':
                    patient_add(new_article)



            except Exception as e:
                print(e)
                continue
        else:
            print(new_article_form.errors)
            continue

def first_add(request):
    spr=Spider()
    infor_list_t_l_d=spr.more_list_page_data(2)
    bath_add(infor_list_t_l_d)
    return HttpResponse('finish')


def get_new(request):
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

    bath_add(new_article_list)
    return HttpResponse('finish')



def patient_add(a_artical):
    content=a_artical.content
    patient_address_list=extract_data(a_artical.content)
    if a_artical.about_patient.all().count()==0:
        for address in patient_address_list:
            new_patinet=Patient(address_now=address,article_related_id=a_artical.id)
            new_patinet.save()

            print('New patient added !!!!!',new_patinet,address)


    elif len(patient_address_list) == a_artical.about_patient.all().count():
        print('The patinets of this Article was added')













