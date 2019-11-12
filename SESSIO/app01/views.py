from django.shortcuts import render,HttpResponse,redirect
from app01 import models

# Create your views here.


def login(request):
    if request.method==" GET":
        return render(request,"login.html")
    username=request.POST.get('username')
    password=request.POST.get("password")
    new_obj=models.Userinfo.objects.filter(username=username,password=password).first()
    if new_obj:
        # result=redirect('/index/')
        # result.set_cookie('SESSIO',username)
        # return result

        request.session['username']=new_obj.username
        request.session['user_id']=new_obj.pk
        # print(new_obj.pk)
        # print(request.session.keys())
        # print(request.session.values())
        # print(request.session.items())
        del request.session['user_id']
        print(request.session.items())
        # print(request.session.session_key())
        return redirect('/index/')


    return render(request,'login.html',{'error':'Wrong Information!'})




def query(request):
    models.Userinfo.objects.create(
        username='donald',
        password='1946',
    )
    return HttpResponse("DONE")
def auth(f):
    def inner(request,*args,**kwargs):
        username = request.session.get('username')
        if not username:
            # return render(request, 'login.html')
            return redirect('/login/')
        ret=f(request,*args,**kwargs)
        return ret
    return inner

@auth
def index(request):

    return render(request,'index.html')