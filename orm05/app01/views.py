from django.shortcuts import render,HttpResponse,redirect

# Create your views here.



def wrapper(f):
    def inner(request,*args,**kwargs):
        status=request.session.get('is_login')
        if status:
            ret=f(request,*args,**kwargs)
            return ret
        else:
            return redirect('/login/')

    return inner


def index(request):
    print('this is a index function!')


    return render(request,'index.html')




def login(request):

    if request.method=='GET':
        print('this is a login function!')
        return render(request,'login.html')
    username=request.POST.get('username')
    password=request.POST.get('password')
    if username=='donald' and password=='1946':
        request.session['is_login']=True
        return redirect('/home/')
    else:
        return redirect('/login/')



def home(request):
    print('this is the home function')

    return HttpResponse('HOME')


