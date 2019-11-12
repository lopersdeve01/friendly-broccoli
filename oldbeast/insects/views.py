from django.shortcuts import render,HttpResponse,redirect
from django import forms
from django.http import JsonResponse
from insects import models
import hashlib
from django.conf import settings
import re
from multiselectfield.forms.fields import MultiSelectFormField
from insects import myforms
from django.db.models import Q
from utils.page import DQpage
from django.urls import reverse
from django.views import View
import copy

# 集中处理model表单的表格样式处理

class Customer(forms.ModelForm):
    class Meta:
        model=models.Customer
        fields='__all__'
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for i_name,i in self.field.items():
            print(type(i))
            if not isinstance(i,MultiSelectFormField):  #多选框。出现select与checkbox中出现multiple的加下面格式会出现前端样式走行，所以排除
                i.widget.attrs.update({'class':'form-control'})


# Create your views here.

class UserInfo(forms.Form):
    username=forms.CharField(max_length=12,
                             min_length=4,
                             initial='OLDBEAST',
                             widget=forms.widgets.TextInput(attrs={'class':'username','placeholder':'your username','autocomplete':'off'}),
                             error_messages={
                                 'required': '不能为空',
                                 'min_length': '太短了',
                                 'max_length': '太长了',
                            },
                             )
    password=forms.CharField(max_length=32,
                             error_messages={
                                 'required': '不能为空',
                                 'min_length': '太短了',
                                 'max_length': '太长了',
                             },
                             widget=forms.PasswordInput(attrs={'class':'password','placeholder':'input your password','oncontextmenu':'return false','onpaste':'return false'})

                             )
    confirm_password=forms.CharField(max_length=32,
                               error_messages={
                                   'required': '不能为空',
                                   'min_length': '太短了',
                                   'max_length': '太长了',
                               },
                               widget=forms.PasswordInput(
                                   attrs={'class': 'confirm_password', 'placeholder': 'input your password again',
                                          'oncontextmenu': 'return false', 'onpaste': 'return false'})
                               )
    telephone=forms.CharField(max_length=11,
                              min_length=11,
                              error_messages={
                                  'max_length': '不能太长,需11位',
                                  'min_length': '不能太短,需11位',
                                  'required': '不能为空'
                              },
                              widget=forms.TextInput(
                                  attrs={'class': 'phone_number', 'placeholder': 'input your telephone_number', 'autocomplete': 'off',
                                         'id': 'number'})

                              )

    email=forms.EmailField(
        error_messages={
            'invalid': '必须是邮箱格式',
            'required': '不能为空'
        },
        widget=forms.EmailInput(
            attrs={'class': 'email', 'placeholder': 'input your email-address',
                   'oncontextmenu': 'return false', 'onpaste': 'return false'}))
    # is_active=forms.BooleanField(
    #     widget=forms.NullBooleanSelect( attrs={'class': 'email', 'placeholder': 'input your email-address',
    #                'oncontextmenu': 'return false', 'onpaste': 'return false'}))))
    # depart=forms.CharField(max_length=32)


    def clean(self):
            password=self.cleaned_data.get('password')
            confirm_password=self.cleaned_data.get('confirm_password')
            if password==confirm_password:
                return self.cleaned_data
            else:
                self.add_error('confirm_password','两次密码不一致!')



def md5(a):
    secret_key = 'username'.encode('utf-8')
    ret=hashlib.md5(secret_key)
    ret.update(a.encode('utf-8'))
    return ret.hexdigest()



def login(request):
    data={}
    if request.method=='GET':
        obj=UserInfo()
        return render(request, 'login/login.html', {'obj':obj})
    else:
        # obj=UserInfo(request.POST)
        username = request.POST.get('username')
        print(username)
        password = request.POST.get('password')
        print(password)
        obj= models.UserInfo.objects.filter(username=username, password=md5(password))
        #         # if obj.is_valid():
        #     # print('正确数据', obj.cleaned_data)
        # else:
        #     print('错误信息', obj.errors)
        print(obj)
        if obj:
            request.session['username']=username
            data.update({'status':1,'home':'/home/'})
            obj1=models.Customer.objects.all()

            # return render(request,'customers/home.html',{'obj':obj1})
            return redirect('/customers/')
        else:
            data.update({'status':0,'error':'wrong information!'})
            return redirect('/login/')

        # return JsonResponse(data)
        # return render(request,'login/login.html', {'obj':obj})



def register(request):
    if request.method == 'GET':
        obj = UserInfo()
        return render(request, 'login/register.html', {'obj': obj})
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        obj = UserInfo(request.POST)
        print(obj)

        if obj.is_valid():
            print('正确数据', obj.cleaned_data)
            confirm_password= obj.cleaned_data.get('confirm_password')
            print(confirm_password)
            obj.cleaned_data.pop('confirm_password')

            password=obj.cleaned_data.get('password')
            obj.cleaned_data.update({'password':md5(password)})

            models.UserInfo.objects.create(**obj.cleaned_data)

            return render(request, 'login/login.html', {'obj': obj})
        else:
            print('错误信息', obj.errors)
            return render(request, 'login/register.html', {'obj': obj})




def home(request):
    return render(request,'customers/home.html')


def start(request):
    return render(request,'start.html')


# def customer(request):
#     obj=models.Customer.objects.all()
#     # print(obj)
#     # print()
#     return render(request, 'customers/customers.html', {'obj':obj})

def add(request):
    if request.method=='GET':
        obj=Customer()
        return render(request,'customers/add.html',{'obj':obj})
    else:
        obj=Customer(request.POST)
        if obj.is_valid():
            obj.save()
            return redirect('/customer/')
        else:
            return render(request,'customers/add.html', {'obj': obj})


def edit(request,n):
    obj = models.Customer.objects.filter(pk=n).first()
    print(n)
    obj1 = Customer(instance=obj)
    # print(obj)
    if request.method=='GET':
        return render(request,'customers/edit.html',{'obj':obj1})
    else:
        obj1 = Customer(request.POST,instance=obj)
        obj1.save()
        return render(request, 'customers/edit.html', {'obj': obj1})
#
# def addedit(request,n=None):
#     label="edit" if n else 'add'
#     obj = models.Customer.objects.filter(pk=n).first()
#     print(n)
#     obj1 = Customer(instance=obj)
#     print(obj)
#     if request.method=='GET':
#         return render(request,'customers/edit.html',{'obj':obj1,'label':label})
#     else:
#         obj1 = Customer(request.POST,instance=obj)
#         obj1.save()
#         return render(request, 'customers/edit.html', {'obj': obj1,'label':label})
#
#
def delete(request,n):
    models.Customer.objects.filter(pk=n).first().is_active='false'
    print(models.Customer.objects.filter(pk=n).first())
    return redirect('customer')

# def customers(request):
#
#     select = request.GET.get('select')  # select ————search_field
#     if select:
#         content = request.GET.get('content')  # content____keyword
#         # # print(content)
#         # c_length=len(content)
#         # content1=content[0:c_length+1]
#         # print(content1)
#         if select == '1':
#             obj = models.Customer.objects.filter(name__icontains=content)
#         else:
#             obj = models.Customer.objects.filter(qq__icontains=content)
#         # print(obj)
#
#         import copy
#         recv_data = copy.copy(request.GET)
#         print(type(recv_data))  # <class 'django.http.request.QueryDict'>
#         # from django.http.request import QueryDict
#         # q = Q()  # 实例化q对象
#         # q.children.append([select,content])  # Q(name__contains='陈')
#         #
#         # obj = models.Customer.objects.filter(q)
#         # print(obj)
#         print(recv_data.urlencode())
#         urlencode = request.GET.urlencode()
#         url = '?' + urlencode
#         print(url)
#         url1= url.replace('page=','') if url  else url
#         print(url1)
#         obj_num = obj.count()
#         print(obj_num)
#         page_shown_num = 5
#         a, b = divmod(obj_num, page_shown_num)
#         page_num = a if not b else a + 1
#         try:
#             page = int(request.GET.get('page'))
#         except Exception:
#             page = 1
#
#
#
#
#         page_shown_rage = page_shown_num // 2
#         if page in range(1, page_num + 1):
#             current_page = page
#         else:
#             current_page = 1
#         if current_page - page_shown_rage <= 0:
#             start_page = 1
#             if current_page + page_shown_rage + 1 >= page_num + 1:
#                 end_page = page_num + 1
#             else:
#                 end_page = current_page + page_shown_rage + 1
#         else:
#             start_page = current_page - page_shown_rage
#             if current_page + page_shown_rage + 1 >= page_num + 1:
#                 end_page = page_num + 1
#             else:
#                 end_page = current_page + page_shown_rage + 1
#         start_obj = (current_page - 1) * page_shown_num
#         if (current_page) * page_shown_num + 1 >= obj_num + 1:
#             end_obj = obj_num + 1
#         else:
#             end_obj = (current_page) * page_shown_num + 1
#         obj1 = obj[start_obj:end_obj]
#         lst = range(start_page, end_page)
#         print(lst)
#         if current_page == 1:
#             pre = 1
#         else:
#             pre = current_page-1
#         if current_page == page_num:
#             next = page_num
#         else:
#             next = current_page + 1
#         return render(request, 'customers.html',
#                       {'obj': obj1, 'page': current_page, 'num': page_shown_num, 'lst': lst, 'page_num': page_num,
#                        'pre': pre, 'next': next, 'url': url1})
#
#     else:
#         obj_num=models.Customer.objects.count()
#         page_shown_num=5
#         a,b=divmod(obj_num,page_shown_num)
#         page_num=a if not b else a+1
#         # print(page_num)
#         n=request.GET.get('page')
#         # print(n)
#         # page=request.GET.get('page')
#         try:
#             page = int(request.GET.get('page'))
#         except Exception:
#             page = 1
#
#
#         # ret=request.GET.get('page')
#         # print(ret)
#         # page=int(ret)
#         # print(page)
#         # print(int(page))
#
#
#         # if not b:
#         #     page_num=a
#         # else:
#         #     page_num=a+1
#         page_shown_rage=page_shown_num//2
#
#         if page in range(1,page_num+1):
#             current_page=page
#         else:
#             current_page=1
#         # print(current_page)
#         if current_page-page_shown_rage<=0:
#             start_page=1
#             if current_page+page_shown_rage+1>=page_num+1:
#                 end_page=page_num+1
#             else:
#                 end_page=current_page+page_shown_rage+1
#         else:
#             start_page = current_page-page_shown_rage
#             if current_page + page_shown_rage + 1 >= page_num + 1:
#                 end_page = page_num + 1
#             else:
#                 end_page = current_page + page_shown_rage + 1
#         start_obj=(current_page-1)*page_shown_num
#         if (current_page)*page_shown_num+1>=obj_num+1:
#             end_obj=obj_num+1
#         else:
#             end_obj=(current_page)*page_shown_num+1
#         obj=models.Customer.objects.all()[start_obj:end_obj]
#         lst=range(start_page,end_page)
#         print(lst)
#         if current_page==1:
#             pre=1
#         else:
#             pre=current_page
#         if current_page==page_num:
#             next=page_num
#         else:
#             next=current_page+1
#         return render(request,'customers.html',{'obj':obj,'page':current_page,'num':page_shown_num,'lst':lst,'page_num':page_num,'pre':pre,'next':next})

class Customers(View):
    def get(self,request):
        print(request.get_full_path())  #/customers/?page=3
        path = request.path
        recv_data = copy.copy(request.GET)
        page = request.GET.get('page')  # 当前页码
        search_field = request.GET.get('search_field')  # 搜索条件
        keyword = request.GET.get('keyword')  # 搜索数据   陈
        username=request.session.get('username')
        if keyword:
            q = Q()  # 实例化q对象
            q.children.append([search_field, keyword])  #
            obj = models.Customer.objects.filter(q)
        else:
            obj = models.Customer.objects.all()

        if path == reverse('customer'):
            # 筛选所有公户的客户信息
            tag = '1'
            obj = obj.filter(consultant__isnull=True)
        else:
            tag = '0'
            obj = obj.filter(consultant__username=request.session.get('username'))

        obj_num = obj.count()
        page_shown_num = settings.PER_PAGE_COUNT
        page_number = settings.PAGE_NUMBER_SHOW

        page_obj = DQpage(page, obj_num, page_shown_num, page_number, recv_data)
        obj_shown = obj[page_obj.start_obj:page_obj.end_obj]
        # self.start_obj=start_obj
        # self.end_obj=end_obj

        page_html = page_obj.page_html_func()

        return render(request, 'customers/customer.html',
                      {'tag': tag, 'obj': page_obj, 'page_html': page_html, 'keyword': keyword,
                       'search_field': search_field,'username':username})

    def post(self, request):
        action = request.POST.get('action')
        cids = request.POST.getlist('cids')  # 选中的客户的

        # customer_list = models.Customer.objects.filter(id__in=cids,consultant__isnull=True)

        if hasattr(self, action):
            ret = getattr(self, action)(request, cids)
            if ret:
                return ret
            else:
                return redirect(request.path)
        else:
            return HttpResponse('你的方法不对!!')


def customer(request):
    title = request.GET.get('select')
    if title:
        content = request.GET.get('content')
        # print(content)
        if title == '1':
            obj = models.Customer.objects.filter(name__icontains=content)
        else:
            obj = models.Customer.objects.filter(qq__icontains=content)
        # print(obj)
        urlencode = request.GET.urlencode()
        url = '?' + urlencode
        print(url)
        obj_num = obj.count()
        # print(obj_num)
        page_shown_num = 5
        a, b = divmod(obj_num, page_shown_num)
        page_num = a if not b else a + 1
        page = request.GET.get('page')
        # print(page)
        page_shown_rage = page_shown_num // 2
        if page in range(1, page_num + 1):
            current_page = page
        else:
            current_page = 1
        if current_page - page_shown_rage <= 0:
            start_page = 1
            if current_page + page_shown_rage + 1 >= page_num + 1:
                end_page = page_num + 1
            else:
                end_page = current_page + page_shown_rage + 1
        else:
            start_page = current_page - page_shown_rage
            if current_page + page_shown_rage + 1 >= page_num + 1:
                end_page = page_num + 1
            else:
                end_page = current_page + page_shown_rage + 1
        start_obj = (current_page - 1) * page_shown_num
        if (current_page) * page_shown_num + 1 >= obj_num + 1:
            end_obj = obj_num + 1
        else:
            end_obj = (current_page) * page_shown_num + 1
        obj1 = obj[start_obj:end_obj]
        lst = range(start_page, end_page)
        print(lst)
        if current_page == 1:
            pre = 1
        else:
            pre = current_page-1
        if current_page == page_num:
            next = page_num
        else:
            next = current_page + 1
        return render(request, 'customers.html',
                      {'obj': obj1, 'page': current_page, 'num': page_shown_num, 'lst': lst, 'page_num': page_num,
                       'pre': pre, 'next': next, 'url': url})

    else:

        return render(request,'customers/customer.html')




def search(request):
    title=request.POST.get('select')
    print(title)
    content=request.POST.get('content')
    obj=models.Customer.objects.filter(title__icontain=content).all()
    return render(request,'customers/customer.html',{'obj':obj})


def choose(request):

    ret=models.Customer.objects.filter(name__icontains='')
    print(ret)
    return HttpResponse("DONE")


# def move(request):
#     lst=['公转私户','私转公户']
#     name = request.session.get('username')
#     user_obj = models.UserInfo.objects.filter(name=name)
#
#     action=request.GET.get('action')
#     if action=='3':
#         obj = models.Customer.objects.filter(consultant_id=None)
#         values_list = request.POST.getlist('move')
#         print(values_list)
#         user_obj = obj.UserInfo.objects.filter(name=name)
#         # models.Customer.objects.filter(consultant_id=None)
#         for i in values_list:
#             models.Customer.objects.filter(pk=i).update(consultant=user_obj)
#
#     else:
#         obj = models.Customer.objects.filter(consultant=user_obj)
#         values_list = request.POST.getlist('move')
#         print(values_list)
#         # models.Customer.objects.filter(consultant_id=None)
#         for i in values_list:
#             models.Customer.objects.filter(pk=i).update(consultant=None)
#         return render(request, 'customers/customers.html', {'obj': obj})



def movechao(request):
    lst=['公转私户','私转公户']
    name = request.session.get('username')
    user_obj = models.UserInfo.objects.filter(name=name)
    label='公户转私户' if  'my' in request.path  else '私户转公户'

    action=request.GET.get('action')
    # if action=='3':
    #     obj = models.Customer.objects.filter(consultant_id=None)
    #     values_list = request.POST.getlist('move')
    #     print(values_list)
    #     user_obj = obj.UserInfo.objects.filter(name=name)
    #     # models.Customer.objects.filter(consultant_id=None)
    #     for i in values_list:
    #         models.Customer.objects.filter(pk=i).update(consultant=user_obj)
    #
    # else:
    #     obj = models.Customer.objects.filter(consultant=user_obj)
    #     values_list = request.POST.getlist('move')
    #     print(values_list)
    #     # models.Customer.objects.filter(consultant_id=None)
    #     for i in values_list:
    #         models.Customer.objects.filter(pk=i).update(consultant=None)
    return render(request, 'customers/customer.html', {'label':label})
def query(request):
    username=request.session.get('username')
    print('username')
    return HttpResponse(username)

def value(request):
    if request.method=="GET":
        return render(request,'login/value.html')
    else:
        value_list=request.POST.getlist('move')
        print(value_list)
        return HttpResponse('Done')





