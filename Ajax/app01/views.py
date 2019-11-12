from django.shortcuts import render,HttpResponse,redirect

# Create your views here.



def login(request):

    if request.method == 'GET':
        return render(request,'login.html')
    else:
        uname = request.POST.get('username')
        pwd = request.POST.get('password')

        if uname == 'donald' and pwd == '1946':

            return HttpResponse('1')
        else:
            return HttpResponse('0')



def home(request):

    return render(request,'home.html')
