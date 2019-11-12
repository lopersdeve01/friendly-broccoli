
import json

from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
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



# from ajaxtest import settings
from django.conf import settings

def upload(request):

    if request.method == 'GET':
        print(settings.BASE_DIR) #/static/

        return render(request,'upload.html')

    else:
        print(request.POST)
        print(request.FILES)
        uname = request.POST.get('username')
        pwd = request.POST.get('password')

        file_obj = request.FILES.get('file')

        print(file_obj.name) #开班典礼.pptx

        with open(file_obj.name,'wb') as f:
            # for i in file_obj:
            #     f.write(i)
            for chunk in file_obj.chunks():
                f.write(chunk)


        return HttpResponse('ok')



def jsontest(request):
    """
    状态码;
        1000 : 登录成功
        1001 : 登录失败

    :param request:
    :return:
    """

    if request.method == 'GET':
        return render(request,'jsontest.html')
    else:
        username = request.POST.get('username')
        pwd = request.POST.get('password')
        ret_data = {'status':None,'msg':None}
        print('>>>>>',request.POST)
        #<QueryDict: {'{"username":"123","password":"123"}': ['']}>
        if username == 'chao' and pwd == '123':
            ret_data['status'] = 1000  # 状态码
            ret_data['msg'] = '登录成功'


        else:
            ret_data['status'] = 1001  # 状态码
            ret_data['msg'] = '登录失败'

        # ret_data_json = json.dumps(ret_data,ensure_ascii=False)
        #
        #
        ret_data1=['aa',11]
        # return HttpResponse(ret_data_json,content_type='application/json')
        # return JsonResponse(ret_data)
        return JsonResponse(ret_data1,safe=False)

# '''
#
# ret = username=123&password=123  -- content-type:...urlencoded
# if content-type == 'urlencoded':
#     res_list = ret.split('&')
#     for i in res_list:
#         k = i.split('=')
#         request.POST[k[0]] = k[1]
# elif content-type=='multipart/form-data':
#     ...
#     request.FILES
#
# elif content-type == 'application/json'
#
# '''


















