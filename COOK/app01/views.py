from django.shortcuts import render,HttpResponse,redirect
from app01 import models
# Create your views here.

def index(request):
    usename=request.COOKIES.get("COOK")
    if not usename:
        return redirect('/login/')
    return render(request,'index.html',{'usename':usename})
def query(request):
    ret=models.Userinfo.objects.create(
        usename="donald",
        password="1946"
    )
    return HttpResponse("Done")

def login(request):
    if request.method=="GET":
        return render(request,'login.html')
    usename=request.POST.get('usename')
    password=request.POST.get('password')
    user_obj=models.Userinfo.objects.filter(usename=usename,password=password).first()
    print(usename,password)
    print(user_obj)
    # user_obj=models.Userinfo.objects.filter(usename=usename,password=password)[0]
    if user_obj:
        result=redirect('/index/')
        result.set_cookie('COOK',usename)
        return result
    return render(request,'login.html',{'error':"wrong information"},{'status':'Landing successfully!'})
