from django.shortcuts import render,HttpResponse,redirect

from app01 import models

# Create your views here.
def add(request):
    authors=models.Author.objects.all()
    publishs=models.Publish.objects.all()
    if request.method=="GET":
        return render(request,"add.html",{'authors':authors,'publishs':publishs})

    # print(request.POST)
    # title=request.POST.get("title")
    # price=request.POST.get("price")
    # publish_date=request.POST.get("publish_date")
    # publish=request.POST.get("publish")

    author=request.POST.getlist('author')#通过name值获得form表单中的前台数据
    publish_id=request.POST.getlist('publish')

    print('author',author)
    print(*author)
    print('publish_id',publish_id)
    data=request.POST.dict()
    print(data)
    print(*data)
    # print(**data)
    # new_author_obj=models.Author.objects.filter(id=data['author'])
    data.pop('author')
    # data.pop('publish_id')
    print(data)



    # new_book_obj = models.Book.objects.create(
    #     title=data['title'],
    #     price=data['price'],
    #     publish_date=data['publish_date'],
    #     author_id= int(*author),
    #     publish_id=int(*publish),
    #     )
    new_book_obj = models.Book.objects.create(**data)
    print(type(new_book_obj))
    new_book_obj.author.add(*author)
    # new_book_obj.publish.add(*publish)



    # models.Book.objects.create(
    #     title=title,
    #     price=price,
    #     publish_date=publish_date,
    #     publish=publish,
    # )

    # book=models.Book.objects.all()
    return render(request,'home.html')


    # return HttpResponse("Done")

def home(request):
    book=models.Book.objects.all()
    # print(book)
    # for j in book:
    #     print(j.author)

    return render(request,"home.html",{"book":book})





def edit(request,n):
    obj=models.Book.objects.get(id=n)     #model对象
    author=models.Author.objects.all()
    publish=models.Publish.objects.all()
    # title=new_obj.title
    #     # price=new_obj.price
    #     # publish_date=new_obj.publish_date
    #     # publish=new_obj.publish
    #     #
    #     #
    #     # title = request.POST.get("title")
    #     # price = request.POST.get("price")
    #     # publish_date = request.POST.get("publish_date")
    #     # publish = request.POST.get("publish")
    #     #
    #     # models.Book.objects.create(
    #     #     title=title,
    #     #     price=price,
    #     #     publish_date=publish_date,
    #     #     publish=publish,
    #     # )
    if request.method=="GET":
         return  render(request,'edit.html',{'obj':obj,'author':author,'publish':publish})
    else:
        obj1 = models.Book.objects.filter(id=n)       #queryset对象
        print(request.POST)
        ret=request.POST.dict()
        print(ret)
        ret.pop('author')
        print(ret)
        obj1.update(**ret)
        author=request.POST.getlist('author')
        obj1.first().author.set(author)
        book = models.Book.objects.all()
        return render(request, "home.html", {"book": book})

from django.http import JsonResponse
# def delete(request,n):
#     print(models.Book.objects) #app01.Book.objects
# book=models.Book.objects.all()
# author=models.Author.objects.all()
#
#     models.Book.objects.filter(id=n).delete()
#     return redirect('home')

# def deletebook(request,id):
#     if request.method=="POST":
#         # book_id=request.POST.get('book_id')
#         # print('book_id',book_id)
#         models.Book.objects.filter(pk=int(id)).delete()
#         data={'status':1}
#         return JsonResponse(data)

def delete(request,n):
    # new_obj=models.Book.create()
    models.Book.objects.filter(id=n).delete()
    book=models.Book.objects.all()
    return render(request,"home.html",{"book":book})


def cancel(request):
    book=models.Book.objects.all()
    author=models.Author.objects.all()

    return render(request,"home.html",{"book":book,'author':author})



def query(request):
    ret=request.body
    ret1=request.path_info
    ret2=request.get_full_path()
    ret3=request.method
    ret4=request.path

    print(ret)
    print(ret1)
    print(ret2)
    print(ret3)
    print(ret4)
    # new_obj=models.Book(
    # title="线性代数",
    # price=24,
    # publish_date="2018-01-11",
    # publish="清华出版社",
    # )
    # new_obj.save()
    # print(new_obj)
    # print(type(new_obj))
    # print(new_obj.title)

    # return HttpResponse("Done")
    # ret=models.Book.objects.create(
    #     title="统计学与概率论",
    #     price=45,
    #     publish_date="2019-01-01",
    #     publish="同济大学出版社",
    # )
    # print(ret)
    # print(type(ret))
    # print(ret[0])
    # print(type(ret[0]))
    # print(ret.title)
    # print(ret.publish_date)
#     lst=['同济大学数学系','上海建桥学院高等数学教研室编','李忠，周建莹','吴玉梅，古佳，康敏','西北工业大学高等数学教材编写组'
# ]
#     obj_lst=[]
#     for i in lst:
#         obj=models.Author(
#         name=i
#     )
#         obj_lst.append(obj)
#         models.Author.objects.bulk_create(obj_lst)
#     lst=['高等教育出版社','中国教育出版社','上海财经大学出版社','北京大学出版社','科学出版社']
#     obj_lst=[]
#     for i in lst:
#         obj=models.Publish(
#         name=i
#     )
#         obj_lst.append(obj)
#         models.Publish.objects.bulk_create(obj_lst)
#     lst=[['高等数学（第七版）','2014-07-01','39.3','1','1'],['高等数学习题全解指南','2014-07-01','45.5','2','2'],['高等数学习题集（第四版）','2018-10-10','43','2','3'],['高等数学(第二版)','2009-08-01','25.2','3','4'],['高等数学（经管类）','2018-07-01','59','4','5'],['高等数学（上下册）','2019-08-01','79','5','5']]
#     obj_lst=[]
#     for i in lst:
#         obj=models.Book(
#         title = i[0],
#         price = i[2],
#         publish_date = i[1],
#         author_id=i[3],
#         publish_id=i[4],
#         )
#         obj_lst.append(obj)
#         models.Book.objects.bulk_create(obj_lst)
#     ret=models.Book.objects.create(
#
#                 title = '高等数学（第七版）',
#                 price = 39.3,
#                 publish_date ='2014-07-01',
#                 author_id=1,
#                 publish_id=1,
#
#     )
    return HttpResponse("DONE")
def action(request):
    # new_obj=models.Book(
    # title="线性代数",
    # price=24,
    # publish_date="2018-01-11",
    # publish="清华出版社",
    # )
    # new_obj.save()
    # print(new_obj)
    #
    # ret = models.Book.objects.filter(id=26)
    # print(ret)        #queryset对象
    # ret.delete()
    # print(type(ret))
    # print(ret.title)
    # print(ret[0])     #moddel对象
    # print(type(ret[0]))
    # print(ret[0].title)
    # print(ret[0].publish_date)
    # print(ret[0].publish)

    # ret.update(price=35)

    # ret1 = models.Book.objects.filter(id=28)[0]
    # ret1.price=46
    # ret1.save()
    # print(ret1.price)
    # ret2 = models.Book.objects.filter(id=28)[0]
    # ret2.delete()
    # print(type(id))

    # if int(id)>=11:
    # #
    ret3 = models.Publish.objects.filter(id__lt=11)
    ret3.delete()
    # ret3 = models.Author.objects.all().delete()
    # ret4=models.Book.objects.all().first()
    # print(type(ret4))
    # ret5=models.Book.objects.all()
    # print(type(ret5))
    # print(ret5[2])
    # print(type(ret5[2]))
    # print(ret5.values_list("title","publish"))
    return HttpResponse("Done")


def login(request):
    if request.method=='GET':
        return render(request,'login.html')
    username=request.POST.get('username')
    password=request.POST.get('password')
    if username=='donald' and password=='1946':
        request.session['username']=username
        request.session['username']=username
        return redirect('/home/')
    else:
        return redirect('/login/')

