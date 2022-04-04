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
    id = models.BigAutoField(primary_key=True)
    article_related=models.ForeignKey(verbose_name='相关报告', to='Article',on_delete=models.CASCADE,related_name='about_patient')
    address_now=models.CharField('现在住址',max_length=30,blank=True)
    add_date = models.DateTimeField('添加日期', auto_now_add=True, )
    edit_date = models.DateTimeField('修改日期', auto_now=True, )

    def __str__(self):
        return '病例'+str(self.id)