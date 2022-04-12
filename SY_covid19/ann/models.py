from django.db import models

# Create your models here.

from django.db import models

# class Article_List(models.Model):
#     type_choice = (('ann', '通知'), ('new_p', '新增加病例'))
#     title=models.CharField('标题',max_length=100,db_index=True)
#     url=models.URLField('文章URL')
#     type = models.CharField('类型', choices=type_choice)
#     pub_date = models.DateField('文章日期')
#     add_date =models.DateField('添加日期',auto_now=True,)
#
#
#     class Meta:
#         ordering = ("-pub_date",)
#
#     def __str__(self):
#         return self.title

class Article(models.Model):
    type_choice=(('ann','通知'),('new_p','新增加病例'),('alert','检测结果异常'))
    id = models.BigAutoField(primary_key=True)
    title=models.CharField('标题',max_length=100,db_index=True)
    url = models.URLField('文章URL',unique=True,db_index=True)
    content=models.TextField('内容',max_length=10000,blank=True)
    source=models.CharField('来源',max_length=100,blank=True)
    type=models.CharField('类型',max_length=10,choices=type_choice)
    pub_date = models.DateField('文章日期')
    add_date = models.DateTimeField('添加日期', auto_now_add=True,)
    edit_date=models.DateTimeField('修改日期',auto_now=True,)

    class Meta:
        ordering = ("-pub_date",)

    def __str__(self):
        return self.title


class Patient(models.Model):
    district_c=(('和平区','和平区'),
                ('沈河区','沈河区'),
                ('大东区','大东区'),
                ('皇姑区','皇姑区'),
                ('铁西区','铁西区'),
                ('苏家屯区','苏家屯区'),
                ('浑南区','浑南区'),
                ('沈北新区','沈北新区'),
                ('于洪区','于洪区'),
                ('辽中区','辽中区'),
                ('康平县','康平县'),
                ('法库县','法库县'),
                ('新民市','新民市')
                )
    id = models.BigAutoField(primary_key=True)
    article_related=models.ForeignKey(verbose_name='相关报告', to='Article',on_delete=models.CASCADE,related_name='about_patient')
    address_now=models.CharField('现在住址',max_length=30,blank=True)
    district=models.CharField('区',max_length=20,choices=district_c,blank=True)
    community=models.ForeignKey(verbose_name='小区',to='Community',on_delete=models.CASCADE,related_name='about_patient')
    definite_date= models.DateField('确诊日期', blank=True, null=True)
    add_date = models.DateTimeField('添加日期', auto_now_add=True, )
    edit_date = models.DateTimeField('修改日期', auto_now=True, )

    class Meta:
        ordering = ("-definite_date",)

    def __str__(self):
        return '病例'+str(self.id)

class Community(models.Model):
    district_c = (('和平区', '和平区'),
                  ('沈河区', '沈河区'),
                  ('大东区', '大东区'),
                  ('皇姑区', '皇姑区'),
                  ('铁西区', '铁西区'),
                  ('苏家屯区', '苏家屯区'),
                  ('浑南区', '浑南区'),
                  ('沈北新区', '沈北新区'),
                  ('于洪区', '于洪区'),
                  ('辽中区', '辽中区'),
                  ('康平县', '康平县'),
                  ('法库县', '法库县'),
                  ('新民市', '新民市')
                  )
    name=models.CharField('小区名',max_length=50,db_index=True)
    district=models.CharField('区',max_length=20,choices=district_c)
    patient_number=models.IntegerField('病人数量',default=0)
    lng=models.CharField('经度',max_length=30)
    lat=models.CharField('纬度',max_length=30)
    add_date = models.DateTimeField('添加日期', auto_now_add=True, )
    edit_date = models.DateTimeField('修改日期', auto_now=True, )

    class Meta:
        ordering = ("-add_date",)

    def __str__(self):
        return str(self.name)