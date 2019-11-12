from django.shortcuts import render,HttpResponse,redirect
from app01 import models

# Create your views here.
def home(request):
    obj=models.Book.objects.all()

    return render(request,'home.html',{'obj':obj})


def login(request):
    obj=models.Book.objects.all()
    if request.method=="GET":
        return render(request,'login.html')
    else:
        username=request.POST.get('username')
        password=request.POST.get('password')


        if username=='chao' and password=='wuchao123':
            request.session['username']=username

            return render(request,'home.html',{'obj':obj})
        else:
            return redirect('/login/')


def add(request):
    book_obj=models.Book.objects.create(



    )
    author_obj=models.Book.objects.create()


def delete(request,n):
    ret=models.Book.objects.filter(id=n)
    ret.delete()
    return HttpResponse('Done')


def edit(request,n):


    return render(request,'home.html',{})

