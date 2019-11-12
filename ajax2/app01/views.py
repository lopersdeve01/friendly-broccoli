from django.shortcuts import render,HttpResponse,redirect

# Create your views here.
def home(request):

    return render(request,'home.html')









def login(request):
    #Edition 1
    # if request.method=="GET":
    #     return render (request,'login.html')
    # username=request.POST.get('username')
    # password=request.POST.get('password')
    # if username=='donald' and password=='donald1946':
    #     return render (request,'home.html')
    # else:
    #     return redirect('/login/')
    #Editon 2
    if request.method=="GET":
        return render (request,'login.html')
    username=request.POST.get('username')
    password=request.POST.get('password')
    if username=='donald' and password=='donald1946':
        return HttpResponse('1')
    else:
        return HttpResponse('0')
