from django.shortcuts import render,HttpResponse,redirect
from app01 import models
# Create your views here.,


def index(request):
    from django.db.models import Avg, Sum, Max, Min, Count, F,Q
    # 一对一
    # 查询一下同济大学数学系的电话号码
    # ret=models.Author.objects.filter(name='同济大学数学系').values("au__telephone")
    # ret=models.AuthorDetail.objects.filter(author__name='同济大学数学系').values('telephone')
    #查找一下763对应的作者姓名
    # ret=models.AuthorDetail.objects.filter(telephone="763").values('author__name')
    #一对多
    #查找一下高等数学（第七版）是那个出版社出版的
    # # ret=models.Book.objects.filter(title='高等数学（第七版）').values('publishs__name')
    # ret=models.Publish.objects.filter(book__title='高等数学（第七版）').values('name')
    #查找一下高等教育出版社出版了那些书
    # ret=models.Book.objects.filter(publishs__name="高等教育出版社").values('title')
    # ret1=models.Publish.objects.filter(name='高等教育出版社').values('book__title')
    #多对多
    #高等数学(第二版)的作者是谁
    # ret=models.Book.objects.filter(title='高等数学(第二版)').values('authors__name')
    # ret1=models.Author.objects.filter(book__title='高等数学(第二版)').values('name')

    #聚合查询
    #统计一下书的均价
    # ret=models.Book.objects.filter(a=Avg('price')).values(a)
    # ret=models.Book.objects.all().aggregate(a=Avg('price'),m=Max('price'))#已经转为字典格式
    # 每个出版社出版的书的平均价格
    # ret1=models.Book.objects.values('publishs__id').annotate(a=Avg('price')) #annotate类似hanving
    #而values类似group by
    # ret=models.Book.objects.values('publishs_id').annotate(a=Avg('price'))
    # ret1=models.Publish.objects.annotate(a=Avg('book__price')).values('a')
    # 前者将分类字段一并显示出，后者仅显示分类的结果，比较局限


    #所有书价格上调100元
    # ret=models.Book.objects.all().update(
    #     price=F('price')+100
    # )
    # ret=models.Book.objects.raw('select * from app01_book where id=2;')
    #
    # ret1=models.Book.objects.filter(Q(id=2)|Q(price__gt=1))

    # 1 查询每个作者的姓名以及出版的书的最高价格
    ret1=models.Author.objects.values('name').annotate(m=Max('book__price'))
    # 2 查询作者id大于2作者的姓名以及出版的书的最高价格
    ret2=models.Author.objects.values('name').annotate(m=Max('book__price')).filter(Q(id__gt=2))
    # 3 查询作者id大于2或者作者年龄大于等于20岁的女作者的姓名以及出版的书的最高价格
    ret3=models.Author.objects.values('name').annotate(m=Max('book__price')).filter(Q(id__gt=2)|Q(age__gt=20))
    # 4 查询每个作者出版的书的最高价格的平均值
    ret4=models.Author.objects.values('name').annotate(m=Max('book__price')).aggregate(a=Avg('m'))
    # 5 每个作者出版的所有书的最高价格以及最高价格的那本书的名称
    ret5=models.Author.objects.values('name').annotate(m=Max('book__price')).values('name','book__price','book__title')





    # ret=models.Book.objects.all().aggregate(a=Avg('price'),m=Max('price'))#已经转为字典格式
    # ret1=models.Author.objects.all().values('id__gt=2').annotate(a='name',b=Avg('book__price'))

    print(ret1,ret2,ret3)
    print(type(ret1))
    print(ret4)
    print(ret5)






    # print(ret,ret1)
















    # ret = models.Author.objects.filter(name='王洋').values('au__telephone')
    # ret = models.AuthorDetail.objects.filter(author__name='王洋').values('telephone')
    # print(ret) #<QuerySet [{'au__telephone': '110'}]> #<QuerySet [{'telephone': '110'}]>
    #

    # 一对多
    # 海狗的怂逼人生这本书是哪个出版社出版的
    # ret = models.Book.objects.filter(title='海狗的怂逼人生').values('publishs__name')
    # print(ret) #<QuerySet [{'publishs__name': '24期出版社'}]>
    # ret = models.Publish.objects.filter(book__title='海狗的怂逼人生').values('name')
    # print(ret) #<QuerySet [{'name': '24期出版社'}]>


    #查询一下24期出版社出版了哪些书
    # ret = models.Publish.objects.filter(name='24期出版社').values('book__title')
    # print(ret) #<QuerySet [{'book__title': '华丽的产后护理'}, {'book__title': '海狗的怂逼人生'}]>

    # ret = models.Book.objects.filter(publishs__name='24期出版社').values('title')
    # print(ret) #<QuerySet [{'title': '华丽的产后护理'}, {'title': '海狗的怂逼人生'}]>

    # 多对多
    #海狗的怂逼人生 是哪些作者写的
    # ret = models.Book.objects.filter(title='海狗的怂逼人生').values('authors__name')
    # print(ret)

    # ret = models.Author.objects.filter(book__title='海狗的怂逼人生').values('name')
    # print(ret) #<QuerySet [{'name': '王洋'}, {'name': '海狗'}]>
    # return render(request,'index.txt',{'x':123,'y':456})


    # related_name
    # 查询一下24期出版社出版了哪些书
    # ret = models.Publish.objects.filter(name='24期出版社').values('xxx__title') #xxx代替反向查询的小写表名
    # print(ret)


    # 聚合查询
    # 统计一下所有书的平均价格
    # ret = models.Book.objects.all().aggregate(a=Avg('price'),m=Max('price'))
    # print(ret) #{'price__avg': 45.1, 'price__max': Decimal('200.00')} python字典格式,也就是说,聚合查询是orm语句的结束

    # 每个出版社出版的书的平均价格
    # 用的是publish表的id字段进行分组
    # ret = models.Book.objects.values('publishs__id').annotate(a=Avg('price'))
    # 用的book表的publishs_id字段进行分组
    # ret = models.Book.objects.values('publishs_id').annotate(a=Avg('price'))
    # print(ret)
    # ret = models.Publish.objects.annotate(a=Avg('book__price')).values('a')
    # print(ret) #<QuerySet [{'a': None}, {'a': 71.166667}, {'a': 6.0}]>

    # 查询一下评论数大于点赞数的书
    # ret = models.Book.objects.all()
    # l1 = []
    # for i in ret:
    #     if i.comment > i.good:
    #         l1.append(i)
    # for j in l1:
    #     print(j.title)

    from django.db.models import Avg, Sum, Max, Min, Count,F

    # ret = models.Book.objects.filter(comment__gt=F('good'))
    # print(ret)

    # 将所有书的价格上调100块
    # ret = models.Book.objects.all()
    # for i in ret:
    #     i.price = i.price+100
    #     i.save()

    # models.Book.objects.all().update(
    #     price=F('price')+100
    # )

    from django.db.models import Avg, Sum, Max, Min, Count, F,Q
    # 查询一下价格大于112块或者评论数大于200的,并且id=2书籍
    # ret = models.Book.objects.filter(price__gt=112,comment__lte=200)
    # 或 |   与 &   非~
    # ret = models.Book.objects.filter(Q(id=2)&Q(Q(price__gt=112)|~Q(comment__lte=200)))
    # print(ret)

    # ret = models.Book.objects.raw('select * from app01_book where id=2;')
    # # print(ret)
    # for i in ret:
    #     print(i.title) #海狗的怂逼人生

    # from django.db import connection
    # cursor = connection.cursor()
    # cursor.execute('select * from app01_book;')
    # print(cursor.fetchall())

    return HttpResponse('ok')


# import pymysql
# conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='666',database='orm02',charset='utf8')
# cursor = conn.cursor()
# cursor.execute('select * from app01_book;')
# cursor.fetchall()
