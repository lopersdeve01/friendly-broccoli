from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from app01 import models

# Create your views here.
def login(request):
    if request.method=='GET':
        return render(request,'login.html')
    else:
        username=request.POST.get('username')
        password=request.POST.get('password')
        if username=='donald' and password=='1946':
            request.session['user']=username

            return redirect('/home/')
        else:
            return render(request,'login.html',{'error':'Wrong Information!Try again!'})

def home(request):
    book=models.Book.objects.all()
    author=models.Author.objects.all()

    publish = models.Publish.objects.all()

    return render(request,'home.html',{'book':book,'author':author,'publish':publish})


# def edit(request,n):
#     if request.method=="GET":
#         book=models.Book.objects.get(nid=n)
#         author=models.Author.objects.all()
#         publish=models.Publish.objects.all()
#         print(author)
#         print(publish)
#         return render(request,'edit.html',{'book':book,'author':author,'publish':publish})
#
#
#     else:
#         # title = request.POST.get('title'),
#         # publishDate = request.POST.get('publishDate'),
#         # price = request.POST.get('price'),
#         # publish_id = request.POST.get('publish_id'),
#         ret = models.Book.objects.filter(nid=n)
#         # print(ret)
#         # data={'title':title,'publishDate':publishDate,'price':price,'publish_id':publish_id}
#         # print(data)
#         data1=request.POST.dict()
#         # print(data1)
#         data1.pop('authors')
#         # print(data1)
#         ret.update(**data1)
#         author=request.POST.getlist('authors')
#         print(author)
#         ret[0].authors.set(author)
#         print(ret)
#
#         book=models.Book.objects.all()
#
#         return redirect('/home/')




def add(request):
    if request.method=='GET':
        author=models.Author.objects.all()
        publish=models.Publish.objects.all()
        return render(request,'add.html',{'author':author,'publish':publish})
    else:
        title=request.POST.get('title')
        publishDate=request.POST.get('publishDate'),
        price=request.POST.get('price'),
        # publish_id=request.POST.get('publish_id'),
        print(title)
        print(publishDate)
        print(price)
        # print(publish_id)
        # print(obj)
        ret=models.Book.objects.create(
        title=request.POST.get('title'),
        publishDate=request.POST.get('publishDate'),
        price=request.POST.get('price'),
        publish_id=request.POST.get('publish_id'),
        )


        author=request.POST.getlist('authors')
        print(author)
        ret.authors.add(*author)
        book=models.Book.objects.all()

        return redirect('/home/')


# def delete(request,n):
#
#     models.Book.objects.filter(nid=n).delete()
#     book = models.Book.objects.all()
#     return render(request, 'home.html', {'book': book})


def delete(request,nid):
    print(nid)
    if request.method=="POST":
        models.Book.objects.filter(pk=int(nid)).delete()
        data={'status':1}
        return JsonResponse(data)


def edit(request,n):
    # if request.method=="GET":
    #     bookn=models.Book.objects.filter(nid=n)
    #     author=models.Author.objects.all()
    #     publish=models.Publish.objects.all()
    #     print(bookn)
    #     print(bookn.title)
    #     print(author)
    #     print(publish)
    # #     return render(request,'home.html',{'bookn':bookn,'author':author,'publish':publish})
    #
    # else:
        # title = request.POST.get('title'),
        # publishDate = request.POST.get('publishDate'),
        # price = request.POST.get('price'),
        # publish_id = request.POST.get('publish_id'),
        ret = models.Book.objects.filter(nid=n)
        data=request.POST.dict()
        data.pop('authors')
        author=request.POST.getlist('authors')
        ret.updata(**data)
            # title=request.POST.get('title'),
            # publishDate=request.POST.get('publishDate'),
            # price=request.POST.get('price'),
            # publish_id=request.POST.get('publish_id'),

        ret[0].authors.set(author)
        home='/home/'
        data={'obj':home}
        return JsonResponse(data)
def test(request):


    return render(request,'test.html')