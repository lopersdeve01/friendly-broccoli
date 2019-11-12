from django.shortcuts import render,HttpResponse,redirect
from app01 import models

# Create your views here.


def query(request):

    # # bulk_create
    # obj_list = []
    #
    # for i in range(20):
    #     obj = models.Book(
    #         title=f'金瓶梅{i}',
    #         price=20+i,
    #         publish_date=f'2019-09-{i+1}',
    #         publish='24期出版社'
    #
    #     )
    #     obj_list.append(obj)
    #
    # models.Book.objects.bulk_create(obj_list)  #批量创建

    # ret = models.Book.objects.filter(title='金瓶梅7',publish='24期出版社') #and多条件查询
    # ret = models.Book.objects.exclude(title__startswith='金瓶梅') #金瓶梅8 查不到数据会报错 :Book matching query does not exist.
    # get() returned more than one Book -- it returned 13!
    # ret = models.Book.objects.all().exclude(title__startswith='金瓶梅')
    # ret = models.Book.objects.all().order_by('id').reverse()  #数据排序之后才能反转

    # ret = models.Book.objects.all().count()
    # ret = models.Book.objects.all().first()
    # ret = models.Book.objects.all().last()
    # ret = models.Book.objects.filter(id=9999).exists() #有结果就是True,没有结果就是False
    # ret = models.Book.objects.filter(id=9).values('title','price')
    # ret = models.Book.objects.all().values_list('title','price')
    # ret = models.Book.objects.all().values()
    # ret = models.Book.objects.values()  #调用values或者values_list的对象是objects控制器,那么返回所有数据

    # ret = models.Book.objects.all().values('publish').distinct()
    # ret = models.Book.objects.filter(price__gt=35)  #大于
    # ret = models.Book.objects.filter(price__gte=35) # 大于等于
    # ret = models.Book.objects.filter(price__lt=35) # 小于等于
    # ret = models.Book.objects.filter(price__lte=35) # 小于等于
    # ret = models.Book.objects.filter(price__range=[35,38]) # 大于等35,小于等于38
    # ret = models.Book.objects.filter(title__contains='金瓶梅') # 字段数据中包含这个字符串的数据都要
    # ret = models.Book.objects.filter(title__contains='金瓶梅')
    # ret = models.Book.objects.filter(title__icontains="python")  # 不区分大小写
    # from app01.models import Book
    # ret = models.Book.objects.filter(title__icontains="python")  # 不区分大小写
    # ret = models.Book.objects.filter(title__startswith="py")  # 以什么开头，istartswith  不区分大小写
    # ret = models.Book.objects.filter(publish_date='2019-09-15')
    ret = models.Book.objects.filter(publish_date__year='2019',publish_date__month='8',publish_date__day='1')
    # ret = models.Book.objects.filter(publish_date__isnull=True) #这个字段值为空的那些数据

    print(ret)



    return HttpResponse('xx')


def showbooks(request):
    """
    查看书籍
    :param request:
    :return:
    """
    all_books = models.Book.objects.all()

    return render(request,'showbooks.html',{'all_books':all_books})


def add_book(request):
    if request.method == 'GET':

        return render(request,'add_book.html')
    else:
        print(request.POST)
        # title = request.POST.get('title')
        # price = request.POST.get('price')
        # publish_date = request.POST.get('publish_date')
        # publish = request.POST.get('publish')
        data = request.POST.dict()  #

        models.Book.objects.create(
            # title=title,
            # price=price,
            # publish_date=publish_date,
            # publish=publish

            **data
        )
        #{'title': ['asdf '], 'price': ['212'], 'publish_date': ['2019-09-12'], 'publish': ['asdf ']}

        return redirect('showbooks')





def delete_book(request,n):
    print(models.Book.objects) #app01.Book.objects
    #要求局部刷新，实现步骤通过ajax，取值，删除，返回重新加载





    models.Book.objects.filter(id=n).delete()

    return redirect('showbooks')


def edit_book(request,n):
    book_obj = models.Book.objects.filter(pk=n)
    if request.method == 'GET':

        return render(request,'edit_book.html',{'book_obj':book_obj.first()})
    else:
        print(request.POST)
        # <QueryDict: {'title': ['金瓶梅7777'], 'price': ['27.00'], 'publish_date': ['2019-09-08'], 'publish': ['24期出版社xx']}>
        ret = request.POST.dict()

        book_obj.update(
            **ret
        )

        return redirect('showbooks')







