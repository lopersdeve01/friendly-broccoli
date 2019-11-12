from django.shortcuts import HttpResponse
from django import forms
import copy
from django.db.models import Q
from django.shortcuts import render, redirect
from django.conf import settings
from web import models
from django.views import View
from web.page import Page
from collections import OrderedDict
from django.forms import modelformset_factory,formset_factory
from web.routes import get_all_url_dict
from web.forms.forms import MultiPermissionForm
from django.utils.safestring import mark_safe
# from web.icon_crawl import icon_list
from web.models import Permission, Role
from django.http import JsonResponse



class Customer(forms.ModelForm):
    class Meta:
        model=models.Customer
        fields='__all__'
        labels={'name':'姓名','age':'年龄','email':'邮件','company':'公司'}


def query(request):
    obj_list=[]
    lst='abcdefghijklmnopqrstuvwxyz'
    for i in range(0,len(lst)):
        obj=models.Customer(
            name=lst[i]*3+'1',
            age = 24,
            email = lst[i]*3+'@qq.com',
            company =lst[i]+'.com',
            )
        obj_list.append(obj)
    models.Customer.objects.bulk_create(obj_list)
    return render(request,'base.html')



def login(request):
    if request.method=="GET":
        return  render(request,'login.html')
    else:
        username=request.POST.get('username')
        password=request.POST.get('password')
        obj=models.UserInfo.objects.filter(username=username,password=password)
        # print(obj)
        # print(obj.menu)
        # if obj:
        #     request.session['is_login']=True
        #     request.session['username']= username
        #     ret=models.Role.objects.filter(userinfo__username=username).values('permissions__url','permissions__title',
        #     'permissions__menus__pk','permissions__menus__name', 'permissions__menus__icon','permissions__menus__weight').distinct()
        #     request.session['ret']=list(ret)
        #     print(ret)
        #
        #     # 筛选菜单权限
        #     # menu_list = []
        #     # for i in ret:
        #     #     if i.get('permissions__menu'):
        #     #         menu_list.append(i)
        #     # # 将菜单权限注入到session
        #     # request.session['menu_list'] = menu_list
        #     # 拼接字典
        #     menu_data={}
        #     for i in ret:
        #         if i.get('permissions__menus__pk') in menu_data:
        #             k = i.get('permissions__menus__pk')
        #             # print(i.get('permissions__menus__pk'),i.get('permissions__url'))
        #             # print(k)
        #             # print({'title':i.get('permissions__title'),'url':i.get('permissions__url')})
        #             menu_data[k]['children'].append({'title':i.get('permissions__title'),
        #                                               'url' :i.get('permissions__url')})
        #
        #         else:
        #             k = i.get('permissions__menus__pk')
        #             menu_data[k] = {
        #                 'name': i.get('permissions__menus__name'),
        #                 'icon': i.get('permissions__menus__icon'),
        #                 'weight': i.get('permissions__menus__weight'),
        #                 'children': [
        #                     {'title': i.get('permissions__title'), 'url': i.get('permissions__url')},
        #                 ],
        #             }
        #             # print(11)
        #             # print(i.get('permissions__menus__name'))
        #             # print(22)
        #             # menu_data[k]['name']=i.get('permissions__menus__name') # keyError 找不到key为1的值，无法进行迭代添加子字典值
        #             # menu_data[k]['icon']=i.get('permissions__menus__icon')
        #             # menu_data[k]['weight'] = i.get('permissions__menus__weight')
        #             # menu_data[k]['children'].append({'title': i.get('permissions__title'),
        #             #                             'url': i.get('permissions__url')})
        #     print(menu_data)
        #
        #     # 排序
        #     menu_dict=OrderedDict()
        #     menu_list=sorted(menu_data,key=lambda x:menu_data[x]['weight'],reverse=True)
        #     # 按照menu_data的键中的weight对字典的键进行排序，返回字典键的列表
        #     print(menu_list)
        #     for key in menu_list:
        #         menu_dict[key]=menu_data[key]
            # print(menu_dict)
        #     request.session['menu_dict']=menu_dict

        if obj :
            request.session['is_login']=True
            request.session['username']= username
            ret=models.Role.objects.filter(userinfo__username=username).values('permissions__pk','permissions__url',
            'permissions__title','permissions__parents_id','permissions__reverse_name','permissions__menus__pk',
            'permissions__menus__name', 'permissions__menus__icon','permissions__menus__weight').distinct()

#说明，本个orm菜单系统的菜单标签分为三级，一为系统级别，也就是标题，二是管理级别，
            # 主要是各个系统的内容展示，与一级菜单的关系是将通过外键将一级菜单的系统表格关联在一起，由此可以通过外键跨表查询是否具备一级菜单的外键
            # 来确定是否为为二级菜单，三级菜单与二级菜单的关系为，三级菜单附属在二级菜单的网页上，通过parents_id（二级菜单的id）与二级菜单发生所属关系，
            # 通过检验其是否含有parents_id来确定三级才的身份与归属。
            request.session['ret']=list(ret)                     # 使用list。将queryset转化为可以为python使用形式
            print('ret',ret)
            reverse_names = []                                   #  别名集合
            permission_dict = {}
            menu_data = {}
            for i in ret:
                permission_dict[i.get('permissions__pk')] = i        #二级菜单字典(键为一级菜单的id值menus_id，值为二级菜单)
                reverse_names.append(i.get('permissions__reverse_name'))
                if i.get('permissions__menus__pk'):
                    if i.get('permissions__menus__pk') in menu_data:
                        k = i.get('permissions__menus__pk')
                        # print(i.get('permissions__menus__pk'),i.get('permissions__url'))
                        # print(k)
                        # print({'title':i.get('permissions__title'),'url':i.get('permissions__url')})
                        menu_data[k]['children'].append({'title': i.get('permissions__title'),
                                                         'url': i.get('permissions__url'),
                                                         'parents_id': i.get('permissions__parents_id'),
                                                         'reverse_name': i.get('permissions__reverse_name')})

                    else:
                        k = i.get('permissions__menus__pk')
                        print('permissions__menus__name',i.get('permissions__menus__name'))
                        menu_data[k] = {
                            'pk':i.get('permissions__pk'),
                            'name': i.get('permissions__menus__name'),
                            'icon': i.get('permissions__menus__icon'),
                            'weight': i.get('permissions__menus__weight'),
                            'children': [
                                {'pk':i.get('permissions__pk'),
                                'title': i.get('permissions__title'), 'url': i.get('permissions__url'),
                                 'parents_id': i.get('permissions__parents_id'),
                                 'reverse_name': i.get('permissions__reverse_name')},
                            ],
                        }


            print('menu_data',menu_data)

            # 排序
            menu_dict = OrderedDict()
            # for i in menu_data:
            #     print(menu_data[i]['weight'])

            menu_list = sorted(menu_data, key=lambda x: menu_data[x]['weight'], reverse=True)    # 未经权重排序的字典
            # 按照menu_data的键中的weight对字典的键进行排序，返回字典键的列表
            # print('menu_list',menu_list)
            for key in menu_list:
                menu_dict[key] = menu_data[key]
            # print(menu_dict)
            # request.session['menu_data'] =menu_data
            request.session['reverse_names'] = reverse_names

            request.session['permission_dict'] = permission_dict
            print('menu_dict', menu_dict)  # 权重排序字典
            request.session['menu_dict'] = menu_dict
            # request.session['bread_crumb']=
            # 根绝列表中字典间的顺序，对字典的进行排序，形成有序字典，并封装到session中
            # print('menu_data',menu_data)
            # print('permission_dict',permission_dict)
            # print('reverse_names', reverse_names)

            return redirect('index')
        else:
            return redirect('login')




class Customers(View):
    def get(self,request):
        # page, obj_num, page_shown_num, page_number, recv_data = None
        page_shown_num = settings.PER_PAGE_COUNT
        page_number = settings.PAGE_NUMBER_SHOW
        # print(page_shown_num, page_number)

        select=request.GET.get('select')
        keyword=request.GET.get('keyword')

        if not keyword:
            obj_total = models.Customer.objects.all().filter(delete_status=False)
        else:
            q=Q()
            q.children.append([select, keyword])  #

            # obj_total=models.Customer.objects.filter(*[select,keyword])
            obj_total=models.Customer.objects.filter(q)

        obj_num=obj_total.filter(delete_status=False).count()
        page=request.GET.get('page')
        recv_data=copy.copy(request.GET)

        page_obj=Page(page, obj_num, page_shown_num, page_number, recv_data)
        # print(obj_total)
        # print(obj_total[0:6])
        # print(page_obj.start_obj,page_obj.end_obj)
        obj=obj_total[page_obj.start_obj:page_obj.end_obj]
        # print(obj)

        page_html=page_obj.page_html_func()

        # print(page_html)
        return render(request,'customer_list.html',{'obj':obj,'html':page_html})

    def post(self,request):
        action=request.POST.get('action')
        cid=request.POST.get('cid')
        if hasattr(self,action):
            ret=getattr(self,action)(request,cid)
            if ret:
                return ret
            else:
                return redirect(request.path)
        else:
            return HttpResponse('Wrong Action!')

    def tansgs(self,request,cid):
        username=request.session.get('username')
        models.Customer.objects.filter(pk__in=cid,company__isnull=True).update(company=username)
        return redirect(request.path)
    def transsg(self,request,cid):
        username=request.session.get('username')
        models.Customer.objects.filter(pk__in=cid,company=username).update(company__isnull=True)
        return render(request,'customer_list.html')
    def bulkdel(self,request,cid):
        models.Customer.objects.filter(pk__in=cid).update(delete_status=True)
        return render(request, 'customer_list.html')


# def customer_list(request):
#     if request.method=="GET":
#         obj=models.Customer.objects.filter(delete_status=False)
#         print(obj)
#         return render(request,'customer_list.html',{'obj':obj})


def customer_add_edit(request,n=None):
    if request.method=="GET":
        instance = models.Customer.objects.filter(pk=n).first()
        obj=Customer(instance=instance)
        # print(obj)
        return render(request,'customer_add_edit.html',{'obj':obj})
    else:
        next_path = request.GET.get('next')  #
        print(next_path)
        instance = models.Customer.objects.filter(pk=n).first()
        obj=Customer(request.POST,instance=instance)
        if obj.is_valid():
            obj.save()
            print(request.POST)
            print(obj)
            # return render(request,'customer_list.html', {'obj': obj})
            return redirect(next_path)
        else:
            return render(request,'customer_add_edit.html',{'obj':obj})

def edit_del(request,n=None):
    if request.method == "GET":
        instance = models.Customer.objects.filter(pk=n).first()
        obj = Customer(instance=instance)
        print(obj)
        return render(request, 'customer_add_edit.html', {'obj': obj})
    else:
        next_path = request.GET.get('next')  #
        print(next_path)
        instance = models.Customer.objects.filter(pk=n).first()
        obj = Customer(request.POST, instance=instance)
        if obj.is_valid():
            obj.save()
            print(request.POST)
            print(obj)
            # return render(request,'customer_list.html', {'obj': obj})
            return redirect('customer_list')
        else:
            return redirect(request.path)

    # next_path = request.GET.get('next')  #
    # print(next_path)  # http://127.0.0.1:8000/editcustomer/116/?next=/customers/?search_field=qq__contains&keyword=1&page=4
    # # /customers/?search_field=qq__contains
    # # /customers/?search_field=qq__contains&keyword=1&page=4
    # book_form_obj = myforms.CustomerModelForm(request.POST, instance=old_obj)
    #
    # if book_form_obj.is_valid():
    #     book_form_obj.save()
    #     return redirect(next_path)
    # else:
    #     return render(request, 'customer/editcustomer.html',
    #                   {'book_form_obj': book_form_obj, 'label': label, 'username': username})






# def addEditCustomer(request,n=None):
#     username = request.session.get('username')
#     if request.method == 'GET':
#         old_obj = models.Customer.objects.filter(pk=n).first()
#         book_form_obj = myforms.CustomerModelForm(instance=old_obj)
#         return render(request, 'customer/editcustomer.html', {'book_form_obj': book_form_obj,'label':label,'username':username})
#     else:
#         old_obj = models.Customer.objects.filter(pk=n).first()
#         next_path = request.GET.get('next')  #
#         print(next_path) # http://127.0.0.1:8000/editcustomer/116/?next=/customers/?search_field=qq__contains&keyword=1&page=4
#         # /customers/?search_field=qq__contains
#         # /customers/?search_field=qq__contains&keyword=1&page=4
#         book_form_obj = myforms.CustomerModelForm(request.POST,instance=old_obj)
#         if book_form_obj.is_valid():
#             book_form_obj.save()
#             return redirect(next_path)
#         else:
#             return render(request, 'customer/editcustomer.html', {'book_form_obj': book_form_obj,'label':label,'username':username})


def customer_del(request,n):
    models.Customer.objects.filter(pk=n).update(delete_status=True)
    obj=models.Customer.objects.filter(delete_status=False)
    # return redirect(request.path)
    return redirect('customer_list')


# def addEditEnrollmentRecord(request,n=None):
#     username = request.session.get('username')
#     print(n)
#     label='添加记录' if not n else '编辑记录'
#     old_obj = models.Enrollment.objects.filter(pk=n).first()
#     if request.method == 'GET':
#         obj = Enrollment(instance=old_obj)
#         return render(request,'enrollment_record/add_edit_enroll_record.html',{'obj':obj,'label':label,'username':username})
#     else:
#         if not n:
#            obj = Enrollment(request.POST)
#            print(request.POST)
#            obj.save()
#            return redirect('sales:enrollmentrecords')
#         else:
#            obj = Enrollment(request.POST,instance=old_obj)
#            if obj.is_valid():
#                print(request.POST)
#                obj.save()
#                return redirect('sales:enrollmentrecords')
#            else:
#                # print(obj)
#                return render(request, 'enrollment_record/add_edit_enroll_record.html', {'obj': obj,'username':username})











# def customer_list(request):
#     """
#     客户列表
#     :return:
#     """
#     data_list = models.Customer.objects.all()
#
#     return render(request, 'customer_list.html', {'data_list': data_list})


# def customer_add(request):
#     """
#     编辑客户
#     :return:
#     """
#     if request.method == 'GET':
#         form = CustomerForm()
#         return render(request, 'customer_add_edit.html', {'form': form})
#     form = CustomerForm(data=request.POST)
#     if form.is_valid():
#         form.save()
#         return redirect('/customer/list/')
#     return render(request, 'customer_add_edit.html', {'form': form})
#
#
# def customer_edit(request, cid):
#     """
#     新增客户
#     :return:
#     """
#     obj = models.Customer.objects.get(id=cid)
#     if request.method == 'GET':
#         form = CustomerForm(instance=obj)
#         return render(request, 'customer_add_edit.html', {'form': form})
#     form = CustomerForm(data=request.POST, instance=obj)
#     if form.is_valid():
#         form.save()
#         return redirect('/customer/list/')
#     return render(request, 'customer_add_edit.html', {'form': form})


# def customer_del(request, cid):
#     """
#     删除客户
#     :param request:
#     :param cid:
#     :return:
#     """
#     models.Customer.objects.filter(id=cid).delete()
#     return redirect('/customer/list/')




# def login(request):
#
#     if request.method == 'GET':
#         return render(request,'login.html')
#     else:
#         uname = request.POST.get('username')
#         pwd = request.POST.get('password')
#
#         user_obj = models.UserInfo.objects.filter(username=uname,password=pwd)
#         if user_obj:
#             user_obj = user_obj.first()
#             # 登录认证标识
#             request.session['is_login'] = True
#
#             # 登录成功之后，将该用户所有的权限(url)全部注入到session中
#             permission_list = models.Role.objects.filter(userinfo__username=user_obj.username)\
#                 .values('permissions__url','permissions__title','permissions__menu','permissions__icon').distinct()
#             request.session['permission_list'] = list(permission_list)  # Object of type 'QuerySet' is not JSON serializable
#
#             # 筛选菜单权限
#             menu_list = []
#             for permission in permission_list:
#                 if permission.get('permissions__menu'):
#                     menu_list.append(permission)
#             # 将菜单权限注入到session
#             request.session['menu_list'] = menu_list
#
#             print(menu_list)
#             # models.UserInfo.objects.filter(username=user_obj.username).values('roles__permissons__url')
#             # models.Permission.objects.filter(role__userinfo__username=user_obj.username).values('url')
#             # print(permission_list)
#             # [{'permissons__url': '/customer/list/'},
#             # {'permissons__url': '/customer/add/'},
#             # {'permissons__url': '/customer/edit/(?P<cid>\\d+)/'},
#             # {'permissons__url': '/customer/del/(?P<cid>\\d+)/'},
#             # {'permissons__url': '/payment/list/'},
#             # {'permissons__url': '/customer/list/'}]
#
#             return redirect('index')
#
#
#         else:
#             return redirect('login')


def index(request):

    return render(request,'index.html')


class Roles(forms.ModelForm):
    class Meta:
        model = models.Role
        fields = '__all__'
        exclude = ['permissions', ]
        labels = {'name': '姓名', 'permissions': '权限', }
        widgets = {
            # 'name': forms.TextInput(max_length=32),
            # 'weight': forms.TextInput(attrs={'class': 'form-control'}),
            # # 'icon':forms.TextInput(attrs={'class':'form-control'}),
            # 'icon': forms.RadioSelect(choices=[[i[0], mark_safe(i[1])] for i in icon_list]),
            # 'title': forms.TextInput(attrs={'type': 'text'})





            'name': forms.TextInput(attrs={'class': 'form-control','type':'text'}),
        }



def role_list(request):
    obj=models.Role.objects.all()
    return render(request,'role_list.html',{'obj':obj})

def role_add_edit(request,n=None):
    obj = models.Role.objects.filter(pk=n).first()
    if request.method=='GET':
        obj1=Roles(instance=obj)
        return render(request,'role_add_edit.html',{'obj':obj1})
    else:

        obj1=Roles(request.POST,instance=obj)
        if obj1.is_valid():

            obj1.save()
            return redirect('/role_list/')
        else:
            return render(request,'role_add_edit.html',{'obj':obj})

def role_del(request,n):
    models.Role.objects.filter(pk=n).delete()
    return redirect('/role_list/')



# icon_list = [['fa-address-book', '<i aria-hidden="true" class="fa fa-address-book"></i>'], ['fa-address-book-o', '<i aria-hidden="true" class="fa fa-address-book-o"></i>'], ['fa-address-card', '<i aria-hidden="true" class="fa fa-address-card"></i>'], ['fa-address-card-o', '<i aria-hidden="true" class="fa fa-address-card-o"></i>'], ['fa-adjust', '<i aria-hidden="true" class="fa fa-adjust"></i>'], ['fa-american-sign-language-interpreting', '<i aria-hidden="true" class="fa fa-american-sign-language-interpreting"></i>'], ['fa-anchor', '<i aria-hidden="true" class="fa fa-anchor"></i>'], ['fa-archive', '<i aria-hidden="true" class="fa fa-archive"></i>'], ['fa-area-chart', '<i aria-hidden="true" class="fa fa-area-chart"></i>'], ['fa-arrows', '<i aria-hidden="true" class="fa fa-arrows"></i>'], ['fa-arrows-h', '<i aria-hidden="true" class="fa fa-arrows-h"></i>'], ['fa-arrows-v', '<i aria-hidden="true" class="fa fa-arrows-v"></i>'], ['fa-asl-interpreting', '<i aria-hidden="true" class="fa fa-asl-interpreting"></i>'], ['fa-assistive-listening-systems', '<i aria-hidden="true" class="fa fa-assistive-listening-systems"></i>'], ['fa-asterisk', '<i aria-hidden="true" class="fa fa-asterisk"></i>'], ['fa-at', '<i aria-hidden="true" class="fa fa-at"></i>'], ['fa-audio-description', '<i aria-hidden="true" class="fa fa-audio-description"></i>'], ['fa-automobile', '<i aria-hidden="true" class="fa fa-automobile"></i>'], ['fa-balance-scale', '<i aria-hidden="true" class="fa fa-balance-scale"></i>'], ['fa-ban', '<i aria-hidden="true" class="fa fa-ban"></i>'], ['fa-bank', '<i aria-hidden="true" class="fa fa-bank"></i>'], ['fa-bar-chart', '<i aria-hidden="true" class="fa fa-bar-chart"></i>'], ['fa-bar-chart-o', '<i aria-hidden="true" class="fa fa-bar-chart-o"></i>'], ['fa-barcode', '<i aria-hidden="true" class="fa fa-barcode"></i>'], ['fa-bars', '<i aria-hidden="true" class="fa fa-bars"></i>'], ['fa-bath', '<i aria-hidden="true" class="fa fa-bath"></i>'], ['fa-bathtub', '<i aria-hidden="true" class="fa fa-bathtub"></i>'], ['fa-battery', '<i aria-hidden="true" class="fa fa-battery"></i>'], ['fa-battery-0', '<i aria-hidden="true" class="fa fa-battery-0"></i>'], ['fa-battery-1', '<i aria-hidden="true" class="fa fa-battery-1"></i>'], ['fa-battery-2', '<i aria-hidden="true" class="fa fa-battery-2"></i>'], ['fa-battery-3', '<i aria-hidden="true" class="fa fa-battery-3"></i>'], ['fa-battery-4', '<i aria-hidden="true" class="fa fa-battery-4"></i>'], ['fa-battery-empty', '<i aria-hidden="true" class="fa fa-battery-empty"></i>'], ['fa-battery-full', '<i aria-hidden="true" class="fa fa-battery-full"></i>'], ['fa-battery-half', '<i aria-hidden="true" class="fa fa-battery-half"></i>'], ['fa-battery-quarter', '<i aria-hidden="true" class="fa fa-battery-quarter"></i>'], ['fa-battery-three-quarters', '<i aria-hidden="true" class="fa fa-battery-three-quarters"></i>'], ['fa-bed', '<i aria-hidden="true" class="fa fa-bed"></i>'], ['fa-beer', '<i aria-hidden="true" class="fa fa-beer"></i>'], ['fa-bell', '<i aria-hidden="true" class="fa fa-bell"></i>'], ['fa-bell-o', '<i aria-hidden="true" class="fa fa-bell-o"></i>'], ['fa-bell-slash', '<i aria-hidden="true" class="fa fa-bell-slash"></i>'], ['fa-bell-slash-o', '<i aria-hidden="true" class="fa fa-bell-slash-o"></i>'], ['fa-bicycle', '<i aria-hidden="true" class="fa fa-bicycle"></i>'], ['fa-binoculars', '<i aria-hidden="true" class="fa fa-binoculars"></i>'], ['fa-birthday-cake', '<i aria-hidden="true" class="fa fa-birthday-cake"></i>'], ['fa-blind', '<i aria-hidden="true" class="fa fa-blind"></i>'], ['fa-bluetooth', '<i aria-hidden="true" class="fa fa-bluetooth"></i>'], ['fa-bluetooth-b', '<i aria-hidden="true" class="fa fa-bluetooth-b"></i>'], ['fa-bolt', '<i aria-hidden="true" class="fa fa-bolt"></i>'], ['fa-bomb', '<i aria-hidden="true" class="fa fa-bomb"></i>'], ['fa-book', '<i aria-hidden="true" class="fa fa-book"></i>'], ['fa-bookmark', '<i aria-hidden="true" class="fa fa-bookmark"></i>'], ['fa-bookmark-o', '<i aria-hidden="true" class="fa fa-bookmark-o"></i>'], ['fa-braille', '<i aria-hidden="true" class="fa fa-braille"></i>'], ['fa-briefcase', '<i aria-hidden="true" class="fa fa-briefcase"></i>'], ['fa-bug', '<i aria-hidden="true" class="fa fa-bug"></i>'], ['fa-building', '<i aria-hidden="true" class="fa fa-building"></i>'], ['fa-building-o', '<i aria-hidden="true" class="fa fa-building-o"></i>'], ['fa-bullhorn', '<i aria-hidden="true" class="fa fa-bullhorn"></i>'], ['fa-bullseye', '<i aria-hidden="true" class="fa fa-bullseye"></i>'], ['fa-bus', '<i aria-hidden="true" class="fa fa-bus"></i>'], ['fa-cab', '<i aria-hidden="true" class="fa fa-cab"></i>'], ['fa-calculator', '<i aria-hidden="true" class="fa fa-calculator"></i>'], ['fa-calendar', '<i aria-hidden="true" class="fa fa-calendar"></i>'], ['fa-calendar-check-o', '<i aria-hidden="true" class="fa fa-calendar-check-o"></i>'], ['fa-calendar-minus-o', '<i aria-hidden="true" class="fa fa-calendar-minus-o"></i>'], ['fa-calendar-o', '<i aria-hidden="true" class="fa fa-calendar-o"></i>'], ['fa-calendar-plus-o', '<i aria-hidden="true" class="fa fa-calendar-plus-o"></i>'], ['fa-calendar-times-o', '<i aria-hidden="true" class="fa fa-calendar-times-o"></i>'], ['fa-camera', '<i aria-hidden="true" class="fa fa-camera"></i>'], ['fa-camera-retro', '<i aria-hidden="true" class="fa fa-camera-retro"></i>'], ['fa-car', '<i aria-hidden="true" class="fa fa-car"></i>'], ['fa-caret-square-o-down', '<i aria-hidden="true" class="fa fa-caret-square-o-down"></i>'], ['fa-caret-square-o-left', '<i aria-hidden="true" class="fa fa-caret-square-o-left"></i>'], ['fa-caret-square-o-right', '<i aria-hidden="true" class="fa fa-caret-square-o-right"></i>'], ['fa-caret-square-o-up', '<i aria-hidden="true" class="fa fa-caret-square-o-up"></i>'], ['fa-cart-arrow-down', '<i aria-hidden="true" class="fa fa-cart-arrow-down"></i>'], ['fa-cart-plus', '<i aria-hidden="true" class="fa fa-cart-plus"></i>'], ['fa-cc', '<i aria-hidden="true" class="fa fa-cc"></i>'], ['fa-certificate', '<i aria-hidden="true" class="fa fa-certificate"></i>'], ['fa-check', '<i aria-hidden="true" class="fa fa-check"></i>'], ['fa-check-circle', '<i aria-hidden="true" class="fa fa-check-circle"></i>'], ['fa-check-circle-o', '<i aria-hidden="true" class="fa fa-check-circle-o"></i>'], ['fa-check-square', '<i aria-hidden="true" class="fa fa-check-square"></i>'], ['fa-check-square-o', '<i aria-hidden="true" class="fa fa-check-square-o"></i>'], ['fa-child', '<i aria-hidden="true" class="fa fa-child"></i>'], ['fa-circle', '<i aria-hidden="true" class="fa fa-circle"></i>'], ['fa-circle-o', '<i aria-hidden="true" class="fa fa-circle-o"></i>'], ['fa-circle-o-notch', '<i aria-hidden="true" class="fa fa-circle-o-notch"></i>'], ['fa-circle-thin', '<i aria-hidden="true" class="fa fa-circle-thin"></i>'], ['fa-clock-o', '<i aria-hidden="true" class="fa fa-clock-o"></i>'], ['fa-clone', '<i aria-hidden="true" class="fa fa-clone"></i>'], ['fa-close', '<i aria-hidden="true" class="fa fa-close"></i>'], ['fa-cloud', '<i aria-hidden="true" class="fa fa-cloud"></i>'], ['fa-cloud-download', '<i aria-hidden="true" class="fa fa-cloud-download"></i>'], ['fa-cloud-upload', '<i aria-hidden="true" class="fa fa-cloud-upload"></i>'], ['fa-code', '<i aria-hidden="true" class="fa fa-code"></i>'], ['fa-code-fork', '<i aria-hidden="true" class="fa fa-code-fork"></i>'], ['fa-coffee', '<i aria-hidden="true" class="fa fa-coffee"></i>'], ['fa-cog', '<i aria-hidden="true" class="fa fa-cog"></i>'], ['fa-cogs', '<i aria-hidden="true" class="fa fa-cogs"></i>'], ['fa-comment', '<i aria-hidden="true" class="fa fa-comment"></i>'], ['fa-comment-o', '<i aria-hidden="true" class="fa fa-comment-o"></i>'], ['fa-commenting', '<i aria-hidden="true" class="fa fa-commenting"></i>'], ['fa-commenting-o', '<i aria-hidden="true" class="fa fa-commenting-o"></i>'], ['fa-comments', '<i aria-hidden="true" class="fa fa-comments"></i>'], ['fa-comments-o', '<i aria-hidden="true" class="fa fa-comments-o"></i>'], ['fa-compass', '<i aria-hidden="true" class="fa fa-compass"></i>'], ['fa-copyright', '<i aria-hidden="true" class="fa fa-copyright"></i>'], ['fa-creative-commons', '<i aria-hidden="true" class="fa fa-creative-commons"></i>'], ['fa-credit-card', '<i aria-hidden="true" class="fa fa-credit-card"></i>'], ['fa-credit-card-alt', '<i aria-hidden="true" class="fa fa-credit-card-alt"></i>'], ['fa-crop', '<i aria-hidden="true" class="fa fa-crop"></i>'], ['fa-crosshairs', '<i aria-hidden="true" class="fa fa-crosshairs"></i>'], ['fa-cube', '<i aria-hidden="true" class="fa fa-cube"></i>'], ['fa-cubes', '<i aria-hidden="true" class="fa fa-cubes"></i>'], ['fa-cutlery', '<i aria-hidden="true" class="fa fa-cutlery"></i>'], ['fa-dashboard', '<i aria-hidden="true" class="fa fa-dashboard"></i>'], ['fa-database', '<i aria-hidden="true" class="fa fa-database"></i>'], ['fa-deaf', '<i aria-hidden="true" class="fa fa-deaf"></i>'], ['fa-deafness', '<i aria-hidden="true" class="fa fa-deafness"></i>'], ['fa-desktop', '<i aria-hidden="true" class="fa fa-desktop"></i>'], ['fa-diamond', '<i aria-hidden="true" class="fa fa-diamond"></i>'], ['fa-dot-circle-o', '<i aria-hidden="true" class="fa fa-dot-circle-o"></i>'], ['fa-download', '<i aria-hidden="true" class="fa fa-download"></i>'], ['fa-drivers-license', '<i aria-hidden="true" class="fa fa-drivers-license"></i>'], ['fa-drivers-license-o', '<i aria-hidden="true" class="fa fa-drivers-license-o"></i>'], ['fa-edit', '<i aria-hidden="true" class="fa fa-edit"></i>'], ['fa-ellipsis-h', '<i aria-hidden="true" class="fa fa-ellipsis-h"></i>'], ['fa-ellipsis-v', '<i aria-hidden="true" class="fa fa-ellipsis-v"></i>'], ['fa-envelope', '<i aria-hidden="true" class="fa fa-envelope"></i>'], ['fa-envelope-o', '<i aria-hidden="true" class="fa fa-envelope-o"></i>'], ['fa-envelope-open', '<i aria-hidden="true" class="fa fa-envelope-open"></i>'], ['fa-envelope-open-o', '<i aria-hidden="true" class="fa fa-envelope-open-o"></i>'], ['fa-envelope-square', '<i aria-hidden="true" class="fa fa-envelope-square"></i>'], ['fa-eraser', '<i aria-hidden="true" class="fa fa-eraser"></i>'], ['fa-exchange', '<i aria-hidden="true" class="fa fa-exchange"></i>'], ['fa-exclamation', '<i aria-hidden="true" class="fa fa-exclamation"></i>'], ['fa-exclamation-circle', '<i aria-hidden="true" class="fa fa-exclamation-circle"></i>'], ['fa-exclamation-triangle', '<i aria-hidden="true" class="fa fa-exclamation-triangle"></i>'], ['fa-external-link', '<i aria-hidden="true" class="fa fa-external-link"></i>'], ['fa-external-link-square', '<i aria-hidden="true" class="fa fa-external-link-square"></i>'], ['fa-eye', '<i aria-hidden="true" class="fa fa-eye"></i>'], ['fa-eye-slash', '<i aria-hidden="true" class="fa fa-eye-slash"></i>'], ['fa-eyedropper', '<i aria-hidden="true" class="fa fa-eyedropper"></i>'], ['fa-fax', '<i aria-hidden="true" class="fa fa-fax"></i>'], ['fa-feed', '<i aria-hidden="true" class="fa fa-feed"></i>'], ['fa-female', '<i aria-hidden="true" class="fa fa-female"></i>'], ['fa-fighter-jet', '<i aria-hidden="true" class="fa fa-fighter-jet"></i>'], ['fa-file-archive-o', '<i aria-hidden="true" class="fa fa-file-archive-o"></i>'], ['fa-file-audio-o', '<i aria-hidden="true" class="fa fa-file-audio-o"></i>'], ['fa-file-code-o', '<i aria-hidden="true" class="fa fa-file-code-o"></i>'], ['fa-file-excel-o', '<i aria-hidden="true" class="fa fa-file-excel-o"></i>'], ['fa-file-image-o', '<i aria-hidden="true" class="fa fa-file-image-o"></i>'], ['fa-file-movie-o', '<i aria-hidden="true" class="fa fa-file-movie-o"></i>'], ['fa-file-pdf-o', '<i aria-hidden="true" class="fa fa-file-pdf-o"></i>'], ['fa-file-photo-o', '<i aria-hidden="true" class="fa fa-file-photo-o"></i>'], ['fa-file-picture-o', '<i aria-hidden="true" class="fa fa-file-picture-o"></i>'], ['fa-file-powerpoint-o', '<i aria-hidden="true" class="fa fa-file-powerpoint-o"></i>'], ['fa-file-sound-o', '<i aria-hidden="true" class="fa fa-file-sound-o"></i>'], ['fa-file-video-o', '<i aria-hidden="true" class="fa fa-file-video-o"></i>'], ['fa-file-word-o', '<i aria-hidden="true" class="fa fa-file-word-o"></i>'], ['fa-file-zip-o', '<i aria-hidden="true" class="fa fa-file-zip-o"></i>'], ['fa-film', '<i aria-hidden="true" class="fa fa-film"></i>'], ['fa-filter', '<i aria-hidden="true" class="fa fa-filter"></i>'], ['fa-fire', '<i aria-hidden="true" class="fa fa-fire"></i>'], ['fa-fire-extinguisher', '<i aria-hidden="true" class="fa fa-fire-extinguisher"></i>'], ['fa-flag', '<i aria-hidden="true" class="fa fa-flag"></i>'], ['fa-flag-checkered', '<i aria-hidden="true" class="fa fa-flag-checkered"></i>'], ['fa-flag-o', '<i aria-hidden="true" class="fa fa-flag-o"></i>'], ['fa-flash', '<i aria-hidden="true" class="fa fa-flash"></i>'], ['fa-flask', '<i aria-hidden="true" class="fa fa-flask"></i>'], ['fa-folder', '<i aria-hidden="true" class="fa fa-folder"></i>'], ['fa-folder-o', '<i aria-hidden="true" class="fa fa-folder-o"></i>'], ['fa-folder-open', '<i aria-hidden="true" class="fa fa-folder-open"></i>'], ['fa-folder-open-o', '<i aria-hidden="true" class="fa fa-folder-open-o"></i>'], ['fa-frown-o', '<i aria-hidden="true" class="fa fa-frown-o"></i>'], ['fa-futbol-o', '<i aria-hidden="true" class="fa fa-futbol-o"></i>'], ['fa-gamepad', '<i aria-hidden="true" class="fa fa-gamepad"></i>'], ['fa-gavel', '<i aria-hidden="true" class="fa fa-gavel"></i>'], ['fa-gear', '<i aria-hidden="true" class="fa fa-gear"></i>'], ['fa-gears', '<i aria-hidden="true" class="fa fa-gears"></i>'], ['fa-gift', '<i aria-hidden="true" class="fa fa-gift"></i>'], ['fa-glass', '<i aria-hidden="true" class="fa fa-glass"></i>'], ['fa-globe', '<i aria-hidden="true" class="fa fa-globe"></i>'], ['fa-graduation-cap', '<i aria-hidden="true" class="fa fa-graduation-cap"></i>'], ['fa-group', '<i aria-hidden="true" class="fa fa-group"></i>'], ['fa-hand-grab-o', '<i aria-hidden="true" class="fa fa-hand-grab-o"></i>'], ['fa-hand-lizard-o', '<i aria-hidden="true" class="fa fa-hand-lizard-o"></i>'], ['fa-hand-paper-o', '<i aria-hidden="true" class="fa fa-hand-paper-o"></i>'], ['fa-hand-peace-o', '<i aria-hidden="true" class="fa fa-hand-peace-o"></i>'], ['fa-hand-pointer-o', '<i aria-hidden="true" class="fa fa-hand-pointer-o"></i>'], ['fa-hand-rock-o', '<i aria-hidden="true" class="fa fa-hand-rock-o"></i>'], ['fa-hand-scissors-o', '<i aria-hidden="true" class="fa fa-hand-scissors-o"></i>'], ['fa-hand-spock-o', '<i aria-hidden="true" class="fa fa-hand-spock-o"></i>'], ['fa-hand-stop-o', '<i aria-hidden="true" class="fa fa-hand-stop-o"></i>'], ['fa-handshake-o', '<i aria-hidden="true" class="fa fa-handshake-o"></i>'], ['fa-hard-of-hearing', '<i aria-hidden="true" class="fa fa-hard-of-hearing"></i>'], ['fa-hashtag', '<i aria-hidden="true" class="fa fa-hashtag"></i>'], ['fa-hdd-o', '<i aria-hidden="true" class="fa fa-hdd-o"></i>'], ['fa-headphones', '<i aria-hidden="true" class="fa fa-headphones"></i>'], ['fa-heart', '<i aria-hidden="true" class="fa fa-heart"></i>'], ['fa-heart-o', '<i aria-hidden="true" class="fa fa-heart-o"></i>'], ['fa-heartbeat', '<i aria-hidden="true" class="fa fa-heartbeat"></i>'], ['fa-history', '<i aria-hidden="true" class="fa fa-history"></i>'], ['fa-home', '<i aria-hidden="true" class="fa fa-home"></i>'], ['fa-hotel', '<i aria-hidden="true" class="fa fa-hotel"></i>'], ['fa-hourglass', '<i aria-hidden="true" class="fa fa-hourglass"></i>'], ['fa-hourglass-1', '<i aria-hidden="true" class="fa fa-hourglass-1"></i>'], ['fa-hourglass-2', '<i aria-hidden="true" class="fa fa-hourglass-2"></i>'], ['fa-hourglass-3', '<i aria-hidden="true" class="fa fa-hourglass-3"></i>'], ['fa-hourglass-end', '<i aria-hidden="true" class="fa fa-hourglass-end"></i>'], ['fa-hourglass-half', '<i aria-hidden="true" class="fa fa-hourglass-half"></i>'], ['fa-hourglass-o', '<i aria-hidden="true" class="fa fa-hourglass-o"></i>'], ['fa-hourglass-start', '<i aria-hidden="true" class="fa fa-hourglass-start"></i>'], ['fa-i-cursor', '<i aria-hidden="true" class="fa fa-i-cursor"></i>'], ['fa-id-badge', '<i aria-hidden="true" class="fa fa-id-badge"></i>'], ['fa-id-card', '<i aria-hidden="true" class="fa fa-id-card"></i>'], ['fa-id-card-o', '<i aria-hidden="true" class="fa fa-id-card-o"></i>'], ['fa-image', '<i aria-hidden="true" class="fa fa-image"></i>'], ['fa-inbox', '<i aria-hidden="true" class="fa fa-inbox"></i>'], ['fa-industry', '<i aria-hidden="true" class="fa fa-industry"></i>'], ['fa-info', '<i aria-hidden="true" class="fa fa-info"></i>'], ['fa-info-circle', '<i aria-hidden="true" class="fa fa-info-circle"></i>'], ['fa-institution', '<i aria-hidden="true" class="fa fa-institution"></i>'], ['fa-key', '<i aria-hidden="true" class="fa fa-key"></i>'], ['fa-keyboard-o', '<i aria-hidden="true" class="fa fa-keyboard-o"></i>'], ['fa-language', '<i aria-hidden="true" class="fa fa-language"></i>'], ['fa-laptop', '<i aria-hidden="true" class="fa fa-laptop"></i>'], ['fa-leaf', '<i aria-hidden="true" class="fa fa-leaf"></i>'], ['fa-legal', '<i aria-hidden="true" class="fa fa-legal"></i>'], ['fa-lemon-o', '<i aria-hidden="true" class="fa fa-lemon-o"></i>'], ['fa-level-down', '<i aria-hidden="true" class="fa fa-level-down"></i>'], ['fa-level-up', '<i aria-hidden="true" class="fa fa-level-up"></i>'], ['fa-life-bouy', '<i aria-hidden="true" class="fa fa-life-bouy"></i>'], ['fa-life-buoy', '<i aria-hidden="true" class="fa fa-life-buoy"></i>'], ['fa-life-ring', '<i aria-hidden="true" class="fa fa-life-ring"></i>'], ['fa-life-saver', '<i aria-hidden="true" class="fa fa-life-saver"></i>'], ['fa-lightbulb-o', '<i aria-hidden="true" class="fa fa-lightbulb-o"></i>'], ['fa-line-chart', '<i aria-hidden="true" class="fa fa-line-chart"></i>'], ['fa-location-arrow', '<i aria-hidden="true" class="fa fa-location-arrow"></i>'], ['fa-lock', '<i aria-hidden="true" class="fa fa-lock"></i>'], ['fa-low-vision', '<i aria-hidden="true" class="fa fa-low-vision"></i>'], ['fa-magic', '<i aria-hidden="true" class="fa fa-magic"></i>'], ['fa-magnet', '<i aria-hidden="true" class="fa fa-magnet"></i>'], ['fa-mail-forward', '<i aria-hidden="true" class="fa fa-mail-forward"></i>'], ['fa-mail-reply', '<i aria-hidden="true" class="fa fa-mail-reply"></i>'], ['fa-mail-reply-all', '<i aria-hidden="true" class="fa fa-mail-reply-all"></i>'], ['fa-male', '<i aria-hidden="true" class="fa fa-male"></i>'], ['fa-map', '<i aria-hidden="true" class="fa fa-map"></i>'], ['fa-map-marker', '<i aria-hidden="true" class="fa fa-map-marker"></i>'], ['fa-map-o', '<i aria-hidden="true" class="fa fa-map-o"></i>'], ['fa-map-pin', '<i aria-hidden="true" class="fa fa-map-pin"></i>'], ['fa-map-signs', '<i aria-hidden="true" class="fa fa-map-signs"></i>'], ['fa-meh-o', '<i aria-hidden="true" class="fa fa-meh-o"></i>'], ['fa-microchip', '<i aria-hidden="true" class="fa fa-microchip"></i>'], ['fa-microphone', '<i aria-hidden="true" class="fa fa-microphone"></i>'], ['fa-microphone-slash', '<i aria-hidden="true" class="fa fa-microphone-slash"></i>'], ['fa-minus', '<i aria-hidden="true" class="fa fa-minus"></i>'], ['fa-minus-circle', '<i aria-hidden="true" class="fa fa-minus-circle"></i>'], ['fa-minus-square', '<i aria-hidden="true" class="fa fa-minus-square"></i>'], ['fa-minus-square-o', '<i aria-hidden="true" class="fa fa-minus-square-o"></i>'], ['fa-mobile', '<i aria-hidden="true" class="fa fa-mobile"></i>'], ['fa-mobile-phone', '<i aria-hidden="true" class="fa fa-mobile-phone"></i>'], ['fa-money', '<i aria-hidden="true" class="fa fa-money"></i>'], ['fa-moon-o', '<i aria-hidden="true" class="fa fa-moon-o"></i>'], ['fa-mortar-board', '<i aria-hidden="true" class="fa fa-mortar-board"></i>'], ['fa-motorcycle', '<i aria-hidden="true" class="fa fa-motorcycle"></i>'], ['fa-mouse-pointer', '<i aria-hidden="true" class="fa fa-mouse-pointer"></i>'], ['fa-music', '<i aria-hidden="true" class="fa fa-music"></i>'], ['fa-navicon', '<i aria-hidden="true" class="fa fa-navicon"></i>'], ['fa-newspaper-o', '<i aria-hidden="true" class="fa fa-newspaper-o"></i>'], ['fa-object-group', '<i aria-hidden="true" class="fa fa-object-group"></i>'], ['fa-object-ungroup', '<i aria-hidden="true" class="fa fa-object-ungroup"></i>'], ['fa-paint-brush', '<i aria-hidden="true" class="fa fa-paint-brush"></i>'], ['fa-paper-plane', '<i aria-hidden="true" class="fa fa-paper-plane"></i>'], ['fa-paper-plane-o', '<i aria-hidden="true" class="fa fa-paper-plane-o"></i>'], ['fa-paw', '<i aria-hidden="true" class="fa fa-paw"></i>'], ['fa-pencil', '<i aria-hidden="true" class="fa fa-pencil"></i>'], ['fa-pencil-square', '<i aria-hidden="true" class="fa fa-pencil-square"></i>'], ['fa-pencil-square-o', '<i aria-hidden="true" class="fa fa-pencil-square-o"></i>'], ['fa-percent', '<i aria-hidden="true" class="fa fa-percent"></i>'], ['fa-phone', '<i aria-hidden="true" class="fa fa-phone"></i>'], ['fa-phone-square', '<i aria-hidden="true" class="fa fa-phone-square"></i>'], ['fa-photo', '<i aria-hidden="true" class="fa fa-photo"></i>'], ['fa-picture-o', '<i aria-hidden="true" class="fa fa-picture-o"></i>'], ['fa-pie-chart', '<i aria-hidden="true" class="fa fa-pie-chart"></i>'], ['fa-plane', '<i aria-hidden="true" class="fa fa-plane"></i>'], ['fa-plug', '<i aria-hidden="true" class="fa fa-plug"></i>'], ['fa-plus', '<i aria-hidden="true" class="fa fa-plus"></i>'], ['fa-plus-circle', '<i aria-hidden="true" class="fa fa-plus-circle"></i>'], ['fa-plus-square', '<i aria-hidden="true" class="fa fa-plus-square"></i>'], ['fa-plus-square-o', '<i aria-hidden="true" class="fa fa-plus-square-o"></i>'], ['fa-podcast', '<i aria-hidden="true" class="fa fa-podcast"></i>'], ['fa-power-off', '<i aria-hidden="true" class="fa fa-power-off"></i>'], ['fa-print', '<i aria-hidden="true" class="fa fa-print"></i>'], ['fa-puzzle-piece', '<i aria-hidden="true" class="fa fa-puzzle-piece"></i>'], ['fa-qrcode', '<i aria-hidden="true" class="fa fa-qrcode"></i>'], ['fa-question', '<i aria-hidden="true" class="fa fa-question"></i>'], ['fa-question-circle', '<i aria-hidden="true" class="fa fa-question-circle"></i>'], ['fa-question-circle-o', '<i aria-hidden="true" class="fa fa-question-circle-o"></i>'], ['fa-quote-left', '<i aria-hidden="true" class="fa fa-quote-left"></i>'], ['fa-quote-right', '<i aria-hidden="true" class="fa fa-quote-right"></i>'], ['fa-random', '<i aria-hidden="true" class="fa fa-random"></i>'], ['fa-recycle', '<i aria-hidden="true" class="fa fa-recycle"></i>'], ['fa-refresh', '<i aria-hidden="true" class="fa fa-refresh"></i>'], ['fa-registered', '<i aria-hidden="true" class="fa fa-registered"></i>'], ['fa-remove', '<i aria-hidden="true" class="fa fa-remove"></i>'], ['fa-reorder', '<i aria-hidden="true" class="fa fa-reorder"></i>'], ['fa-reply', '<i aria-hidden="true" class="fa fa-reply"></i>'], ['fa-reply-all', '<i aria-hidden="true" class="fa fa-reply-all"></i>'], ['fa-retweet', '<i aria-hidden="true" class="fa fa-retweet"></i>'], ['fa-road', '<i aria-hidden="true" class="fa fa-road"></i>'], ['fa-rocket', '<i aria-hidden="true" class="fa fa-rocket"></i>'], ['fa-rss', '<i aria-hidden="true" class="fa fa-rss"></i>'], ['fa-rss-square', '<i aria-hidden="true" class="fa fa-rss-square"></i>'], ['fa-s15', '<i aria-hidden="true" class="fa fa-s15"></i>'], ['fa-search', '<i aria-hidden="true" class="fa fa-search"></i>'], ['fa-search-minus', '<i aria-hidden="true" class="fa fa-search-minus"></i>'], ['fa-search-plus', '<i aria-hidden="true" class="fa fa-search-plus"></i>'], ['fa-send', '<i aria-hidden="true" class="fa fa-send"></i>'], ['fa-send-o', '<i aria-hidden="true" class="fa fa-send-o"></i>'], ['fa-server', '<i aria-hidden="true" class="fa fa-server"></i>'], ['fa-share', '<i aria-hidden="true" class="fa fa-share"></i>'], ['fa-share-alt', '<i aria-hidden="true" class="fa fa-share-alt"></i>'], ['fa-share-alt-square', '<i aria-hidden="true" class="fa fa-share-alt-square"></i>'], ['fa-share-square', '<i aria-hidden="true" class="fa fa-share-square"></i>'], ['fa-share-square-o', '<i aria-hidden="true" class="fa fa-share-square-o"></i>'], ['fa-shield', '<i aria-hidden="true" class="fa fa-shield"></i>'], ['fa-ship', '<i aria-hidden="true" class="fa fa-ship"></i>'], ['fa-shopping-bag', '<i aria-hidden="true" class="fa fa-shopping-bag"></i>'], ['fa-shopping-basket', '<i aria-hidden="true" class="fa fa-shopping-basket"></i>'], ['fa-shopping-cart', '<i aria-hidden="true" class="fa fa-shopping-cart"></i>'], ['fa-shower', '<i aria-hidden="true" class="fa fa-shower"></i>'], ['fa-sign-in', '<i aria-hidden="true" class="fa fa-sign-in"></i>'], ['fa-sign-language', '<i aria-hidden="true" class="fa fa-sign-language"></i>'], ['fa-sign-out', '<i aria-hidden="true" class="fa fa-sign-out"></i>'], ['fa-signal', '<i aria-hidden="true" class="fa fa-signal"></i>'], ['fa-signing', '<i aria-hidden="true" class="fa fa-signing"></i>'], ['fa-sitemap', '<i aria-hidden="true" class="fa fa-sitemap"></i>'], ['fa-sliders', '<i aria-hidden="true" class="fa fa-sliders"></i>'], ['fa-smile-o', '<i aria-hidden="true" class="fa fa-smile-o"></i>'], ['fa-snowflake-o', '<i aria-hidden="true" class="fa fa-snowflake-o"></i>'], ['fa-soccer-ball-o', '<i aria-hidden="true" class="fa fa-soccer-ball-o"></i>'], ['fa-sort', '<i aria-hidden="true" class="fa fa-sort"></i>'], ['fa-sort-alpha-asc', '<i aria-hidden="true" class="fa fa-sort-alpha-asc"></i>'], ['fa-sort-alpha-desc', '<i aria-hidden="true" class="fa fa-sort-alpha-desc"></i>'], ['fa-sort-amount-asc', '<i aria-hidden="true" class="fa fa-sort-amount-asc"></i>'], ['fa-sort-amount-desc', '<i aria-hidden="true" class="fa fa-sort-amount-desc"></i>'], ['fa-sort-asc', '<i aria-hidden="true" class="fa fa-sort-asc"></i>'], ['fa-sort-desc', '<i aria-hidden="true" class="fa fa-sort-desc"></i>'], ['fa-sort-down', '<i aria-hidden="true" class="fa fa-sort-down"></i>'], ['fa-sort-numeric-asc', '<i aria-hidden="true" class="fa fa-sort-numeric-asc"></i>'], ['fa-sort-numeric-desc', '<i aria-hidden="true" class="fa fa-sort-numeric-desc"></i>'], ['fa-sort-up', '<i aria-hidden="true" class="fa fa-sort-up"></i>'], ['fa-space-shuttle', '<i aria-hidden="true" class="fa fa-space-shuttle"></i>'], ['fa-spinner', '<i aria-hidden="true" class="fa fa-spinner"></i>'], ['fa-spoon', '<i aria-hidden="true" class="fa fa-spoon"></i>'], ['fa-square', '<i aria-hidden="true" class="fa fa-square"></i>'], ['fa-square-o', '<i aria-hidden="true" class="fa fa-square-o"></i>'], ['fa-star', '<i aria-hidden="true" class="fa fa-star"></i>'], ['fa-star-half', '<i aria-hidden="true" class="fa fa-star-half"></i>'], ['fa-star-half-empty', '<i aria-hidden="true" class="fa fa-star-half-empty"></i>'], ['fa-star-half-full', '<i aria-hidden="true" class="fa fa-star-half-full"></i>'], ['fa-star-half-o', '<i aria-hidden="true" class="fa fa-star-half-o"></i>'], ['fa-star-o', '<i aria-hidden="true" class="fa fa-star-o"></i>'], ['fa-sticky-note', '<i aria-hidden="true" class="fa fa-sticky-note"></i>'], ['fa-sticky-note-o', '<i aria-hidden="true" class="fa fa-sticky-note-o"></i>'], ['fa-street-view', '<i aria-hidden="true" class="fa fa-street-view"></i>'], ['fa-suitcase', '<i aria-hidden="true" class="fa fa-suitcase"></i>'], ['fa-sun-o', '<i aria-hidden="true" class="fa fa-sun-o"></i>'], ['fa-support', '<i aria-hidden="true" class="fa fa-support"></i>'], ['fa-tablet', '<i aria-hidden="true" class="fa fa-tablet"></i>'], ['fa-tachometer', '<i aria-hidden="true" class="fa fa-tachometer"></i>'], ['fa-tag', '<i aria-hidden="true" class="fa fa-tag"></i>'], ['fa-tags', '<i aria-hidden="true" class="fa fa-tags"></i>'], ['fa-tasks', '<i aria-hidden="true" class="fa fa-tasks"></i>'], ['fa-taxi', '<i aria-hidden="true" class="fa fa-taxi"></i>'], ['fa-television', '<i aria-hidden="true" class="fa fa-television"></i>'], ['fa-terminal', '<i aria-hidden="true" class="fa fa-terminal"></i>'], ['fa-thermometer', '<i aria-hidden="true" class="fa fa-thermometer"></i>'], ['fa-thermometer-0', '<i aria-hidden="true" class="fa fa-thermometer-0"></i>'], ['fa-thermometer-1', '<i aria-hidden="true" class="fa fa-thermometer-1"></i>'], ['fa-thermometer-2', '<i aria-hidden="true" class="fa fa-thermometer-2"></i>'], ['fa-thermometer-3', '<i aria-hidden="true" class="fa fa-thermometer-3"></i>'], ['fa-thermometer-4', '<i aria-hidden="true" class="fa fa-thermometer-4"></i>'], ['fa-thermometer-empty', '<i aria-hidden="true" class="fa fa-thermometer-empty"></i>'], ['fa-thermometer-full', '<i aria-hidden="true" class="fa fa-thermometer-full"></i>'], ['fa-thermometer-half', '<i aria-hidden="true" class="fa fa-thermometer-half"></i>'], ['fa-thermometer-quarter', '<i aria-hidden="true" class="fa fa-thermometer-quarter"></i>'], ['fa-thermometer-three-quarters', '<i aria-hidden="true" class="fa fa-thermometer-three-quarters"></i>'], ['fa-thumb-tack', '<i aria-hidden="true" class="fa fa-thumb-tack"></i>'], ['fa-thumbs-down', '<i aria-hidden="true" class="fa fa-thumbs-down"></i>'], ['fa-thumbs-o-down', '<i aria-hidden="true" class="fa fa-thumbs-o-down"></i>'], ['fa-thumbs-o-up', '<i aria-hidden="true" class="fa fa-thumbs-o-up"></i>'], ['fa-thumbs-up', '<i aria-hidden="true" class="fa fa-thumbs-up"></i>'], ['fa-ticket', '<i aria-hidden="true" class="fa fa-ticket"></i>'], ['fa-times', '<i aria-hidden="true" class="fa fa-times"></i>'], ['fa-times-circle', '<i aria-hidden="true" class="fa fa-times-circle"></i>'], ['fa-times-circle-o', '<i aria-hidden="true" class="fa fa-times-circle-o"></i>'], ['fa-times-rectangle', '<i aria-hidden="true" class="fa fa-times-rectangle"></i>'], ['fa-times-rectangle-o', '<i aria-hidden="true" class="fa fa-times-rectangle-o"></i>'], ['fa-tint', '<i aria-hidden="true" class="fa fa-tint"></i>'], ['fa-toggle-down', '<i aria-hidden="true" class="fa fa-toggle-down"></i>'], ['fa-toggle-left', '<i aria-hidden="true" class="fa fa-toggle-left"></i>'], ['fa-toggle-off', '<i aria-hidden="true" class="fa fa-toggle-off"></i>'], ['fa-toggle-on', '<i aria-hidden="true" class="fa fa-toggle-on"></i>'], ['fa-toggle-right', '<i aria-hidden="true" class="fa fa-toggle-right"></i>'], ['fa-toggle-up', '<i aria-hidden="true" class="fa fa-toggle-up"></i>'], ['fa-trademark', '<i aria-hidden="true" class="fa fa-trademark"></i>'], ['fa-trash', '<i aria-hidden="true" class="fa fa-trash"></i>'], ['fa-trash-o', '<i aria-hidden="true" class="fa fa-trash-o"></i>'], ['fa-tree', '<i aria-hidden="true" class="fa fa-tree"></i>'], ['fa-trophy', '<i aria-hidden="true" class="fa fa-trophy"></i>'], ['fa-truck', '<i aria-hidden="true" class="fa fa-truck"></i>'], ['fa-tty', '<i aria-hidden="true" class="fa fa-tty"></i>'], ['fa-tv', '<i aria-hidden="true" class="fa fa-tv"></i>'], ['fa-umbrella', '<i aria-hidden="true" class="fa fa-umbrella"></i>'], ['fa-universal-access', '<i aria-hidden="true" class="fa fa-universal-access"></i>'], ['fa-university', '<i aria-hidden="true" class="fa fa-university"></i>'], ['fa-unlock', '<i aria-hidden="true" class="fa fa-unlock"></i>'], ['fa-unlock-alt', '<i aria-hidden="true" class="fa fa-unlock-alt"></i>'], ['fa-unsorted', '<i aria-hidden="true" class="fa fa-unsorted"></i>'], ['fa-upload', '<i aria-hidden="true" class="fa fa-upload"></i>'], ['fa-user', '<i aria-hidden="true" class="fa fa-user"></i>'], ['fa-user-circle', '<i aria-hidden="true" class="fa fa-user-circle"></i>'], ['fa-user-circle-o', '<i aria-hidden="true" class="fa fa-user-circle-o"></i>'], ['fa-user-o', '<i aria-hidden="true" class="fa fa-user-o"></i>'], ['fa-user-plus', '<i aria-hidden="true" class="fa fa-user-plus"></i>'], ['fa-user-secret', '<i aria-hidden="true" class="fa fa-user-secret"></i>'], ['fa-user-times', '<i aria-hidden="true" class="fa fa-user-times"></i>'], ['fa-users', '<i aria-hidden="true" class="fa fa-users"></i>'], ['fa-vcard', '<i aria-hidden="true" class="fa fa-vcard"></i>'], ['fa-vcard-o', '<i aria-hidden="true" class="fa fa-vcard-o"></i>'], ['fa-video-camera', '<i aria-hidden="true" class="fa fa-video-camera"></i>'], ['fa-volume-control-phone', '<i aria-hidden="true" class="fa fa-volume-control-phone"></i>'], ['fa-volume-down', '<i aria-hidden="true" class="fa fa-volume-down"></i>'], ['fa-volume-off', '<i aria-hidden="true" class="fa fa-volume-off"></i>'], ['fa-volume-up', '<i aria-hidden="true" class="fa fa-volume-up"></i>'], ['fa-warning', '<i aria-hidden="true" class="fa fa-warning"></i>'], ['fa-wheelchair', '<i aria-hidden="true" class="fa fa-wheelchair"></i>'], ['fa-wheelchair-alt', '<i aria-hidden="true" class="fa fa-wheelchair-alt"></i>'], ['fa-wifi', '<i aria-hidden="true" class="fa fa-wifi"></i>'], ['fa-window-close', '<i aria-hidden="true" class="fa fa-window-close"></i>'], ['fa-window-close-o', '<i aria-hidden="true" class="fa fa-window-close-o"></i>'], ['fa-window-maximize', '<i aria-hidden="true" class="fa fa-window-maximize"></i>'], ['fa-window-minimize', '<i aria-hidden="true" class="fa fa-window-minimize"></i>'], ['fa-window-restore', '<i aria-hidden="true" class="fa fa-window-restore"></i>'], ['fa-wrench', '<i aria-hidden="true" class="fa fa-wrench"></i>']]
icon_list =[['fa fa-address-book', '<i aria-hidden="true" class="fa fa-address-book"></i>'], ['fa fa-address-book-o', '<i aria-hidden="true" class="fa fa-address-book-o"></i>'], ['fa fa-address-card', '<i aria-hidden="true" class="fa fa-address-card"></i>'], ['fa fa-address-card-o', '<i aria-hidden="true" class="fa fa-address-card-o"></i>'], ['fa fa-adjust', '<i aria-hidden="true" class="fa fa-adjust"></i>'], ['fa fa-american-sign-language-interpreting', '<i aria-hidden="true" class="fa fa-american-sign-language-interpreting"></i>'], ['fa fa-anchor', '<i aria-hidden="true" class="fa fa-anchor"></i>'], ['fa fa-archive', '<i aria-hidden="true" class="fa fa-archive"></i>'], ['fa fa-area-chart', '<i aria-hidden="true" class="fa fa-area-chart"></i>'], ['fa fa-arrows', '<i aria-hidden="true" class="fa fa-arrows"></i>'], ['fa fa-arrows-h', '<i aria-hidden="true" class="fa fa-arrows-h"></i>'], ['fa fa-arrows-v', '<i aria-hidden="true" class="fa fa-arrows-v"></i>'], ['fa fa-asl-interpreting', '<i aria-hidden="true" class="fa fa-asl-interpreting"></i>'], ['fa fa-assistive-listening-systems', '<i aria-hidden="true" class="fa fa-assistive-listening-systems"></i>'], ['fa fa-asterisk', '<i aria-hidden="true" class="fa fa-asterisk"></i>'], ['fa fa-at', '<i aria-hidden="true" class="fa fa-at"></i>'], ['fa fa-audio-description', '<i aria-hidden="true" class="fa fa-audio-description"></i>'], ['fa fa-automobile', '<i aria-hidden="true" class="fa fa-automobile"></i>'], ['fa fa-balance-scale', '<i aria-hidden="true" class="fa fa-balance-scale"></i>'], ['fa fa-ban', '<i aria-hidden="true" class="fa fa-ban"></i>'], ['fa fa-bank', '<i aria-hidden="true" class="fa fa-bank"></i>'], ['fa fa-bar-chart', '<i aria-hidden="true" class="fa fa-bar-chart"></i>'], ['fa fa-bar-chart-o', '<i aria-hidden="true" class="fa fa-bar-chart-o"></i>'], ['fa fa-barcode', '<i aria-hidden="true" class="fa fa-barcode"></i>'], ['fa fa-bars', '<i aria-hidden="true" class="fa fa-bars"></i>'], ['fa fa-bath', '<i aria-hidden="true" class="fa fa-bath"></i>'], ['fa fa-bathtub', '<i aria-hidden="true" class="fa fa-bathtub"></i>'], ['fa fa-battery', '<i aria-hidden="true" class="fa fa-battery"></i>'], ['fa fa-battery-0', '<i aria-hidden="true" class="fa fa-battery-0"></i>'], ['fa fa-battery-1', '<i aria-hidden="true" class="fa fa-battery-1"></i>'], ['fa fa-battery-2', '<i aria-hidden="true" class="fa fa-battery-2"></i>'], ['fa fa-battery-3', '<i aria-hidden="true" class="fa fa-battery-3"></i>'], ['fa fa-battery-4', '<i aria-hidden="true" class="fa fa-battery-4"></i>'], ['fa fa-battery-empty', '<i aria-hidden="true" class="fa fa-battery-empty"></i>'], ['fa fa-battery-full', '<i aria-hidden="true" class="fa fa-battery-full"></i>'], ['fa fa-battery-half', '<i aria-hidden="true" class="fa fa-battery-half"></i>'], ['fa fa-battery-quarter', '<i aria-hidden="true" class="fa fa-battery-quarter"></i>'], ['fa fa-battery-three-quarters', '<i aria-hidden="true" class="fa fa-battery-three-quarters"></i>'], ['fa fa-bed', '<i aria-hidden="true" class="fa fa-bed"></i>'], ['fa fa-beer', '<i aria-hidden="true" class="fa fa-beer"></i>'], ['fa fa-bell', '<i aria-hidden="true" class="fa fa-bell"></i>'], ['fa fa-bell-o', '<i aria-hidden="true" class="fa fa-bell-o"></i>'], ['fa fa-bell-slash', '<i aria-hidden="true" class="fa fa-bell-slash"></i>'], ['fa fa-bell-slash-o', '<i aria-hidden="true" class="fa fa-bell-slash-o"></i>'], ['fa fa-bicycle', '<i aria-hidden="true" class="fa fa-bicycle"></i>'], ['fa fa-binoculars', '<i aria-hidden="true" class="fa fa-binoculars"></i>'], ['fa fa-birthday-cake', '<i aria-hidden="true" class="fa fa-birthday-cake"></i>'], ['fa fa-blind', '<i aria-hidden="true" class="fa fa-blind"></i>'], ['fa fa-bluetooth', '<i aria-hidden="true" class="fa fa-bluetooth"></i>'], ['fa fa-bluetooth-b', '<i aria-hidden="true" class="fa fa-bluetooth-b"></i>'], ['fa fa-bolt', '<i aria-hidden="true" class="fa fa-bolt"></i>'], ['fa fa-bomb', '<i aria-hidden="true" class="fa fa-bomb"></i>'], ['fa fa-book', '<i aria-hidden="true" class="fa fa-book"></i>'], ['fa fa-bookmark', '<i aria-hidden="true" class="fa fa-bookmark"></i>'], ['fa fa-bookmark-o', '<i aria-hidden="true" class="fa fa-bookmark-o"></i>'], ['fa fa-braille', '<i aria-hidden="true" class="fa fa-braille"></i>'], ['fa fa-briefcase', '<i aria-hidden="true" class="fa fa-briefcase"></i>'], ['fa fa-bug', '<i aria-hidden="true" class="fa fa-bug"></i>'], ['fa fa-building', '<i aria-hidden="true" class="fa fa-building"></i>'], ['fa fa-building-o', '<i aria-hidden="true" class="fa fa-building-o"></i>'], ['fa fa-bullhorn', '<i aria-hidden="true" class="fa fa-bullhorn"></i>'], ['fa fa-bullseye', '<i aria-hidden="true" class="fa fa-bullseye"></i>'], ['fa fa-bus', '<i aria-hidden="true" class="fa fa-bus"></i>'], ['fa fa-cab', '<i aria-hidden="true" class="fa fa-cab"></i>'], ['fa fa-calculator', '<i aria-hidden="true" class="fa fa-calculator"></i>'], ['fa fa-calendar', '<i aria-hidden="true" class="fa fa-calendar"></i>'], ['fa fa-calendar-check-o', '<i aria-hidden="true" class="fa fa-calendar-check-o"></i>'], ['fa fa-calendar-minus-o', '<i aria-hidden="true" class="fa fa-calendar-minus-o"></i>'], ['fa fa-calendar-o', '<i aria-hidden="true" class="fa fa-calendar-o"></i>'], ['fa fa-calendar-plus-o', '<i aria-hidden="true" class="fa fa-calendar-plus-o"></i>'], ['fa fa-calendar-times-o', '<i aria-hidden="true" class="fa fa-calendar-times-o"></i>'], ['fa fa-camera', '<i aria-hidden="true" class="fa fa-camera"></i>'], ['fa fa-camera-retro', '<i aria-hidden="true" class="fa fa-camera-retro"></i>'], ['fa fa-car', '<i aria-hidden="true" class="fa fa-car"></i>'], ['fa fa-caret-square-o-down', '<i aria-hidden="true" class="fa fa-caret-square-o-down"></i>'], ['fa fa-caret-square-o-left', '<i aria-hidden="true" class="fa fa-caret-square-o-left"></i>'], ['fa fa-caret-square-o-right', '<i aria-hidden="true" class="fa fa-caret-square-o-right"></i>'], ['fa fa-caret-square-o-up', '<i aria-hidden="true" class="fa fa-caret-square-o-up"></i>'], ['fa fa-cart-arrow-down', '<i aria-hidden="true" class="fa fa-cart-arrow-down"></i>'], ['fa fa-cart-plus', '<i aria-hidden="true" class="fa fa-cart-plus"></i>'], ['fa fa-cc', '<i aria-hidden="true" class="fa fa-cc"></i>'], ['fa fa-certificate', '<i aria-hidden="true" class="fa fa-certificate"></i>'], ['fa fa-check', '<i aria-hidden="true" class="fa fa-check"></i>'], ['fa fa-check-circle', '<i aria-hidden="true" class="fa fa-check-circle"></i>'], ['fa fa-check-circle-o', '<i aria-hidden="true" class="fa fa-check-circle-o"></i>'], ['fa fa-check-square', '<i aria-hidden="true" class="fa fa-check-square"></i>'], ['fa fa-check-square-o', '<i aria-hidden="true" class="fa fa-check-square-o"></i>'], ['fa fa-child', '<i aria-hidden="true" class="fa fa-child"></i>'], ['fa fa-circle', '<i aria-hidden="true" class="fa fa-circle"></i>'], ['fa fa-circle-o', '<i aria-hidden="true" class="fa fa-circle-o"></i>'], ['fa fa-circle-o-notch', '<i aria-hidden="true" class="fa fa-circle-o-notch"></i>'], ['fa fa-circle-thin', '<i aria-hidden="true" class="fa fa-circle-thin"></i>'], ['fa fa-clock-o', '<i aria-hidden="true" class="fa fa-clock-o"></i>'], ['fa fa-clone', '<i aria-hidden="true" class="fa fa-clone"></i>'], ['fa fa-close', '<i aria-hidden="true" class="fa fa-close"></i>'], ['fa fa-cloud', '<i aria-hidden="true" class="fa fa-cloud"></i>'], ['fa fa-cloud-download', '<i aria-hidden="true" class="fa fa-cloud-download"></i>'], ['fa fa-cloud-upload', '<i aria-hidden="true" class="fa fa-cloud-upload"></i>'], ['fa fa-code', '<i aria-hidden="true" class="fa fa-code"></i>'], ['fa fa-code-fork', '<i aria-hidden="true" class="fa fa-code-fork"></i>'], ['fa fa-coffee', '<i aria-hidden="true" class="fa fa-coffee"></i>'], ['fa fa-cog', '<i aria-hidden="true" class="fa fa-cog"></i>'], ['fa fa-cogs', '<i aria-hidden="true" class="fa fa-cogs"></i>'], ['fa fa-comment', '<i aria-hidden="true" class="fa fa-comment"></i>'], ['fa fa-comment-o', '<i aria-hidden="true" class="fa fa-comment-o"></i>'], ['fa fa-commenting', '<i aria-hidden="true" class="fa fa-commenting"></i>'], ['fa fa-commenting-o', '<i aria-hidden="true" class="fa fa-commenting-o"></i>'], ['fa fa-comments', '<i aria-hidden="true" class="fa fa-comments"></i>'], ['fa fa-comments-o', '<i aria-hidden="true" class="fa fa-comments-o"></i>'], ['fa fa-compass', '<i aria-hidden="true" class="fa fa-compass"></i>'], ['fa fa-copyright', '<i aria-hidden="true" class="fa fa-copyright"></i>'], ['fa fa-creative-commons', '<i aria-hidden="true" class="fa fa-creative-commons"></i>'], ['fa fa-credit-card', '<i aria-hidden="true" class="fa fa-credit-card"></i>'], ['fa fa-credit-card-alt', '<i aria-hidden="true" class="fa fa-credit-card-alt"></i>'], ['fa fa-crop', '<i aria-hidden="true" class="fa fa-crop"></i>'], ['fa fa-crosshairs', '<i aria-hidden="true" class="fa fa-crosshairs"></i>'], ['fa fa-cube', '<i aria-hidden="true" class="fa fa-cube"></i>'], ['fa fa-cubes', '<i aria-hidden="true" class="fa fa-cubes"></i>'], ['fa fa-cutlery', '<i aria-hidden="true" class="fa fa-cutlery"></i>'], ['fa fa-dashboard', '<i aria-hidden="true" class="fa fa-dashboard"></i>'], ['fa fa-database', '<i aria-hidden="true" class="fa fa-database"></i>'], ['fa fa-deaf', '<i aria-hidden="true" class="fa fa-deaf"></i>'], ['fa fa-deafness', '<i aria-hidden="true" class="fa fa-deafness"></i>'], ['fa fa-desktop', '<i aria-hidden="true" class="fa fa-desktop"></i>'], ['fa fa-diamond', '<i aria-hidden="true" class="fa fa-diamond"></i>'], ['fa fa-dot-circle-o', '<i aria-hidden="true" class="fa fa-dot-circle-o"></i>'], ['fa fa-download', '<i aria-hidden="true" class="fa fa-download"></i>'], ['fa fa-drivers-license', '<i aria-hidden="true" class="fa fa-drivers-license"></i>'], ['fa fa-drivers-license-o', '<i aria-hidden="true" class="fa fa-drivers-license-o"></i>'], ['fa fa-edit', '<i aria-hidden="true" class="fa fa-edit"></i>'], ['fa fa-ellipsis-h', '<i aria-hidden="true" class="fa fa-ellipsis-h"></i>'], ['fa fa-ellipsis-v', '<i aria-hidden="true" class="fa fa-ellipsis-v"></i>'], ['fa fa-envelope', '<i aria-hidden="true" class="fa fa-envelope"></i>'], ['fa fa-envelope-o', '<i aria-hidden="true" class="fa fa-envelope-o"></i>'], ['fa fa-envelope-open', '<i aria-hidden="true" class="fa fa-envelope-open"></i>'], ['fa fa-envelope-open-o', '<i aria-hidden="true" class="fa fa-envelope-open-o"></i>'], ['fa fa-envelope-square', '<i aria-hidden="true" class="fa fa-envelope-square"></i>'], ['fa fa-eraser', '<i aria-hidden="true" class="fa fa-eraser"></i>'], ['fa fa-exchange', '<i aria-hidden="true" class="fa fa-exchange"></i>'], ['fa fa-exclamation', '<i aria-hidden="true" class="fa fa-exclamation"></i>'], ['fa fa-exclamation-circle', '<i aria-hidden="true" class="fa fa-exclamation-circle"></i>'], ['fa fa-exclamation-triangle', '<i aria-hidden="true" class="fa fa-exclamation-triangle"></i>'], ['fa fa-external-link', '<i aria-hidden="true" class="fa fa-external-link"></i>'], ['fa fa-external-link-square', '<i aria-hidden="true" class="fa fa-external-link-square"></i>'], ['fa fa-eye', '<i aria-hidden="true" class="fa fa-eye"></i>'], ['fa fa-eye-slash', '<i aria-hidden="true" class="fa fa-eye-slash"></i>'], ['fa fa-eyedropper', '<i aria-hidden="true" class="fa fa-eyedropper"></i>'], ['fa fa-fax', '<i aria-hidden="true" class="fa fa-fax"></i>'], ['fa fa-feed', '<i aria-hidden="true" class="fa fa-feed"></i>'], ['fa fa-female', '<i aria-hidden="true" class="fa fa-female"></i>'], ['fa fa-fighter-jet', '<i aria-hidden="true" class="fa fa-fighter-jet"></i>'], ['fa fa-file-archive-o', '<i aria-hidden="true" class="fa fa-file-archive-o"></i>'], ['fa fa-file-audio-o', '<i aria-hidden="true" class="fa fa-file-audio-o"></i>'], ['fa fa-file-code-o', '<i aria-hidden="true" class="fa fa-file-code-o"></i>'], ['fa fa-file-excel-o', '<i aria-hidden="true" class="fa fa-file-excel-o"></i>'], ['fa fa-file-image-o', '<i aria-hidden="true" class="fa fa-file-image-o"></i>'], ['fa fa-file-movie-o', '<i aria-hidden="true" class="fa fa-file-movie-o"></i>'], ['fa fa-file-pdf-o', '<i aria-hidden="true" class="fa fa-file-pdf-o"></i>'], ['fa fa-file-photo-o', '<i aria-hidden="true" class="fa fa-file-photo-o"></i>'], ['fa fa-file-picture-o', '<i aria-hidden="true" class="fa fa-file-picture-o"></i>'], ['fa fa-file-powerpoint-o', '<i aria-hidden="true" class="fa fa-file-powerpoint-o"></i>'], ['fa fa-file-sound-o', '<i aria-hidden="true" class="fa fa-file-sound-o"></i>'], ['fa fa-file-video-o', '<i aria-hidden="true" class="fa fa-file-video-o"></i>'], ['fa fa-file-word-o', '<i aria-hidden="true" class="fa fa-file-word-o"></i>'], ['fa fa-file-zip-o', '<i aria-hidden="true" class="fa fa-file-zip-o"></i>'], ['fa fa-film', '<i aria-hidden="true" class="fa fa-film"></i>'], ['fa fa-filter', '<i aria-hidden="true" class="fa fa-filter"></i>'], ['fa fa-fire', '<i aria-hidden="true" class="fa fa-fire"></i>'], ['fa fa-fire-extinguisher', '<i aria-hidden="true" class="fa fa-fire-extinguisher"></i>'], ['fa fa-flag', '<i aria-hidden="true" class="fa fa-flag"></i>'], ['fa fa-flag-checkered', '<i aria-hidden="true" class="fa fa-flag-checkered"></i>'], ['fa fa-flag-o', '<i aria-hidden="true" class="fa fa-flag-o"></i>'], ['fa fa-flash', '<i aria-hidden="true" class="fa fa-flash"></i>'], ['fa fa-flask', '<i aria-hidden="true" class="fa fa-flask"></i>'], ['fa fa-folder', '<i aria-hidden="true" class="fa fa-folder"></i>'], ['fa fa-folder-o', '<i aria-hidden="true" class="fa fa-folder-o"></i>'], ['fa fa-folder-open', '<i aria-hidden="true" class="fa fa-folder-open"></i>'], ['fa fa-folder-open-o', '<i aria-hidden="true" class="fa fa-folder-open-o"></i>'], ['fa fa-frown-o', '<i aria-hidden="true" class="fa fa-frown-o"></i>'], ['fa fa-futbol-o', '<i aria-hidden="true" class="fa fa-futbol-o"></i>'], ['fa fa-gamepad', '<i aria-hidden="true" class="fa fa-gamepad"></i>'], ['fa fa-gavel', '<i aria-hidden="true" class="fa fa-gavel"></i>'], ['fa fa-gear', '<i aria-hidden="true" class="fa fa-gear"></i>'], ['fa fa-gears', '<i aria-hidden="true" class="fa fa-gears"></i>'], ['fa fa-gift', '<i aria-hidden="true" class="fa fa-gift"></i>'], ['fa fa-glass', '<i aria-hidden="true" class="fa fa-glass"></i>'], ['fa fa-globe', '<i aria-hidden="true" class="fa fa-globe"></i>'], ['fa fa-graduation-cap', '<i aria-hidden="true" class="fa fa-graduation-cap"></i>'], ['fa fa-group', '<i aria-hidden="true" class="fa fa-group"></i>'], ['fa fa-hand-grab-o', '<i aria-hidden="true" class="fa fa-hand-grab-o"></i>'], ['fa fa-hand-lizard-o', '<i aria-hidden="true" class="fa fa-hand-lizard-o"></i>'], ['fa fa-hand-paper-o', '<i aria-hidden="true" class="fa fa-hand-paper-o"></i>'], ['fa fa-hand-peace-o', '<i aria-hidden="true" class="fa fa-hand-peace-o"></i>'], ['fa fa-hand-pointer-o', '<i aria-hidden="true" class="fa fa-hand-pointer-o"></i>'], ['fa fa-hand-rock-o', '<i aria-hidden="true" class="fa fa-hand-rock-o"></i>'], ['fa fa-hand-scissors-o', '<i aria-hidden="true" class="fa fa-hand-scissors-o"></i>'], ['fa fa-hand-spock-o', '<i aria-hidden="true" class="fa fa-hand-spock-o"></i>'], ['fa fa-hand-stop-o', '<i aria-hidden="true" class="fa fa-hand-stop-o"></i>'], ['fa fa-handshake-o', '<i aria-hidden="true" class="fa fa-handshake-o"></i>'], ['fa fa-hard-of-hearing', '<i aria-hidden="true" class="fa fa-hard-of-hearing"></i>'], ['fa fa-hashtag', '<i aria-hidden="true" class="fa fa-hashtag"></i>'], ['fa fa-hdd-o', '<i aria-hidden="true" class="fa fa-hdd-o"></i>'], ['fa fa-headphones', '<i aria-hidden="true" class="fa fa-headphones"></i>'], ['fa fa-heart', '<i aria-hidden="true" class="fa fa-heart"></i>'], ['fa fa-heart-o', '<i aria-hidden="true" class="fa fa-heart-o"></i>'], ['fa fa-heartbeat', '<i aria-hidden="true" class="fa fa-heartbeat"></i>'], ['fa fa-history', '<i aria-hidden="true" class="fa fa-history"></i>'], ['fa fa-home', '<i aria-hidden="true" class="fa fa-home"></i>'], ['fa fa-hotel', '<i aria-hidden="true" class="fa fa-hotel"></i>'], ['fa fa-hourglass', '<i aria-hidden="true" class="fa fa-hourglass"></i>'], ['fa fa-hourglass-1', '<i aria-hidden="true" class="fa fa-hourglass-1"></i>'], ['fa fa-hourglass-2', '<i aria-hidden="true" class="fa fa-hourglass-2"></i>'], ['fa fa-hourglass-3', '<i aria-hidden="true" class="fa fa-hourglass-3"></i>'], ['fa fa-hourglass-end', '<i aria-hidden="true" class="fa fa-hourglass-end"></i>'], ['fa fa-hourglass-half', '<i aria-hidden="true" class="fa fa-hourglass-half"></i>'], ['fa fa-hourglass-o', '<i aria-hidden="true" class="fa fa-hourglass-o"></i>'], ['fa fa-hourglass-start', '<i aria-hidden="true" class="fa fa-hourglass-start"></i>'], ['fa fa-i-cursor', '<i aria-hidden="true" class="fa fa-i-cursor"></i>'], ['fa fa-id-badge', '<i aria-hidden="true" class="fa fa-id-badge"></i>'], ['fa fa-id-card', '<i aria-hidden="true" class="fa fa-id-card"></i>'], ['fa fa-id-card-o', '<i aria-hidden="true" class="fa fa-id-card-o"></i>'], ['fa fa-image', '<i aria-hidden="true" class="fa fa-image"></i>'], ['fa fa-inbox', '<i aria-hidden="true" class="fa fa-inbox"></i>'], ['fa fa-industry', '<i aria-hidden="true" class="fa fa-industry"></i>'], ['fa fa-info', '<i aria-hidden="true" class="fa fa-info"></i>'], ['fa fa-info-circle', '<i aria-hidden="true" class="fa fa-info-circle"></i>'], ['fa fa-institution', '<i aria-hidden="true" class="fa fa-institution"></i>'], ['fa fa-key', '<i aria-hidden="true" class="fa fa-key"></i>'], ['fa fa-keyboard-o', '<i aria-hidden="true" class="fa fa-keyboard-o"></i>'], ['fa fa-language', '<i aria-hidden="true" class="fa fa-language"></i>'], ['fa fa-laptop', '<i aria-hidden="true" class="fa fa-laptop"></i>'], ['fa fa-leaf', '<i aria-hidden="true" class="fa fa-leaf"></i>'], ['fa fa-legal', '<i aria-hidden="true" class="fa fa-legal"></i>'], ['fa fa-lemon-o', '<i aria-hidden="true" class="fa fa-lemon-o"></i>'], ['fa fa-level-down', '<i aria-hidden="true" class="fa fa-level-down"></i>'], ['fa fa-level-up', '<i aria-hidden="true" class="fa fa-level-up"></i>'], ['fa fa-life-bouy', '<i aria-hidden="true" class="fa fa-life-bouy"></i>'], ['fa fa-life-buoy', '<i aria-hidden="true" class="fa fa-life-buoy"></i>'], ['fa fa-life-ring', '<i aria-hidden="true" class="fa fa-life-ring"></i>'], ['fa fa-life-saver', '<i aria-hidden="true" class="fa fa-life-saver"></i>'], ['fa fa-lightbulb-o', '<i aria-hidden="true" class="fa fa-lightbulb-o"></i>'], ['fa fa-line-chart', '<i aria-hidden="true" class="fa fa-line-chart"></i>'], ['fa fa-location-arrow', '<i aria-hidden="true" class="fa fa-location-arrow"></i>'], ['fa fa-lock', '<i aria-hidden="true" class="fa fa-lock"></i>'], ['fa fa-low-vision', '<i aria-hidden="true" class="fa fa-low-vision"></i>'], ['fa fa-magic', '<i aria-hidden="true" class="fa fa-magic"></i>'], ['fa fa-magnet', '<i aria-hidden="true" class="fa fa-magnet"></i>'], ['fa fa-mail-forward', '<i aria-hidden="true" class="fa fa-mail-forward"></i>'], ['fa fa-mail-reply', '<i aria-hidden="true" class="fa fa-mail-reply"></i>'], ['fa fa-mail-reply-all', '<i aria-hidden="true" class="fa fa-mail-reply-all"></i>'], ['fa fa-male', '<i aria-hidden="true" class="fa fa-male"></i>'], ['fa fa-map', '<i aria-hidden="true" class="fa fa-map"></i>'], ['fa fa-map-marker', '<i aria-hidden="true" class="fa fa-map-marker"></i>'], ['fa fa-map-o', '<i aria-hidden="true" class="fa fa-map-o"></i>'], ['fa fa-map-pin', '<i aria-hidden="true" class="fa fa-map-pin"></i>'], ['fa fa-map-signs', '<i aria-hidden="true" class="fa fa-map-signs"></i>'], ['fa fa-meh-o', '<i aria-hidden="true" class="fa fa-meh-o"></i>'], ['fa fa-microchip', '<i aria-hidden="true" class="fa fa-microchip"></i>'], ['fa fa-microphone', '<i aria-hidden="true" class="fa fa-microphone"></i>'], ['fa fa-microphone-slash', '<i aria-hidden="true" class="fa fa-microphone-slash"></i>'], ['fa fa-minus', '<i aria-hidden="true" class="fa fa-minus"></i>'], ['fa fa-minus-circle', '<i aria-hidden="true" class="fa fa-minus-circle"></i>'], ['fa fa-minus-square', '<i aria-hidden="true" class="fa fa-minus-square"></i>'], ['fa fa-minus-square-o', '<i aria-hidden="true" class="fa fa-minus-square-o"></i>'], ['fa fa-mobile', '<i aria-hidden="true" class="fa fa-mobile"></i>'], ['fa fa-mobile-phone', '<i aria-hidden="true" class="fa fa-mobile-phone"></i>'], ['fa fa-money', '<i aria-hidden="true" class="fa fa-money"></i>'], ['fa fa-moon-o', '<i aria-hidden="true" class="fa fa-moon-o"></i>'], ['fa fa-mortar-board', '<i aria-hidden="true" class="fa fa-mortar-board"></i>'], ['fa fa-motorcycle', '<i aria-hidden="true" class="fa fa-motorcycle"></i>'], ['fa fa-mouse-pointer', '<i aria-hidden="true" class="fa fa-mouse-pointer"></i>'], ['fa fa-music', '<i aria-hidden="true" class="fa fa-music"></i>'], ['fa fa-navicon', '<i aria-hidden="true" class="fa fa-navicon"></i>'], ['fa fa-newspaper-o', '<i aria-hidden="true" class="fa fa-newspaper-o"></i>'], ['fa fa-object-group', '<i aria-hidden="true" class="fa fa-object-group"></i>'], ['fa fa-object-ungroup', '<i aria-hidden="true" class="fa fa-object-ungroup"></i>'], ['fa fa-paint-brush', '<i aria-hidden="true" class="fa fa-paint-brush"></i>'], ['fa fa-paper-plane', '<i aria-hidden="true" class="fa fa-paper-plane"></i>'], ['fa fa-paper-plane-o', '<i aria-hidden="true" class="fa fa-paper-plane-o"></i>'], ['fa fa-paw', '<i aria-hidden="true" class="fa fa-paw"></i>'], ['fa fa-pencil', '<i aria-hidden="true" class="fa fa-pencil"></i>'], ['fa fa-pencil-square', '<i aria-hidden="true" class="fa fa-pencil-square"></i>'], ['fa fa-pencil-square-o', '<i aria-hidden="true" class="fa fa-pencil-square-o"></i>'], ['fa fa-percent', '<i aria-hidden="true" class="fa fa-percent"></i>'], ['fa fa-phone', '<i aria-hidden="true" class="fa fa-phone"></i>'], ['fa fa-phone-square', '<i aria-hidden="true" class="fa fa-phone-square"></i>'], ['fa fa-photo', '<i aria-hidden="true" class="fa fa-photo"></i>'], ['fa fa-picture-o', '<i aria-hidden="true" class="fa fa-picture-o"></i>'], ['fa fa-pie-chart', '<i aria-hidden="true" class="fa fa-pie-chart"></i>'], ['fa fa-plane', '<i aria-hidden="true" class="fa fa-plane"></i>'], ['fa fa-plug', '<i aria-hidden="true" class="fa fa-plug"></i>'], ['fa fa-plus', '<i aria-hidden="true" class="fa fa-plus"></i>'], ['fa fa-plus-circle', '<i aria-hidden="true" class="fa fa-plus-circle"></i>'], ['fa fa-plus-square', '<i aria-hidden="true" class="fa fa-plus-square"></i>'], ['fa fa-plus-square-o', '<i aria-hidden="true" class="fa fa-plus-square-o"></i>'], ['fa fa-podcast', '<i aria-hidden="true" class="fa fa-podcast"></i>'], ['fa fa-power-off', '<i aria-hidden="true" class="fa fa-power-off"></i>'], ['fa fa-print', '<i aria-hidden="true" class="fa fa-print"></i>'], ['fa fa-puzzle-piece', '<i aria-hidden="true" class="fa fa-puzzle-piece"></i>'], ['fa fa-qrcode', '<i aria-hidden="true" class="fa fa-qrcode"></i>'], ['fa fa-question', '<i aria-hidden="true" class="fa fa-question"></i>'], ['fa fa-question-circle', '<i aria-hidden="true" class="fa fa-question-circle"></i>'], ['fa fa-question-circle-o', '<i aria-hidden="true" class="fa fa-question-circle-o"></i>'], ['fa fa-quote-left', '<i aria-hidden="true" class="fa fa-quote-left"></i>'], ['fa fa-quote-right', '<i aria-hidden="true" class="fa fa-quote-right"></i>'], ['fa fa-random', '<i aria-hidden="true" class="fa fa-random"></i>'], ['fa fa-recycle', '<i aria-hidden="true" class="fa fa-recycle"></i>'], ['fa fa-refresh', '<i aria-hidden="true" class="fa fa-refresh"></i>'], ['fa fa-registered', '<i aria-hidden="true" class="fa fa-registered"></i>'], ['fa fa-remove', '<i aria-hidden="true" class="fa fa-remove"></i>'], ['fa fa-reorder', '<i aria-hidden="true" class="fa fa-reorder"></i>'], ['fa fa-reply', '<i aria-hidden="true" class="fa fa-reply"></i>'], ['fa fa-reply-all', '<i aria-hidden="true" class="fa fa-reply-all"></i>'], ['fa fa-retweet', '<i aria-hidden="true" class="fa fa-retweet"></i>'], ['fa fa-road', '<i aria-hidden="true" class="fa fa-road"></i>'], ['fa fa-rocket', '<i aria-hidden="true" class="fa fa-rocket"></i>'], ['fa fa-rss', '<i aria-hidden="true" class="fa fa-rss"></i>'], ['fa fa-rss-square', '<i aria-hidden="true" class="fa fa-rss-square"></i>'], ['fa fa-s15', '<i aria-hidden="true" class="fa fa-s15"></i>'], ['fa fa-search', '<i aria-hidden="true" class="fa fa-search"></i>'], ['fa fa-search-minus', '<i aria-hidden="true" class="fa fa-search-minus"></i>'], ['fa fa-search-plus', '<i aria-hidden="true" class="fa fa-search-plus"></i>'], ['fa fa-send', '<i aria-hidden="true" class="fa fa-send"></i>'], ['fa fa-send-o', '<i aria-hidden="true" class="fa fa-send-o"></i>'], ['fa fa-server', '<i aria-hidden="true" class="fa fa-server"></i>'], ['fa fa-share', '<i aria-hidden="true" class="fa fa-share"></i>'], ['fa fa-share-alt', '<i aria-hidden="true" class="fa fa-share-alt"></i>'], ['fa fa-share-alt-square', '<i aria-hidden="true" class="fa fa-share-alt-square"></i>'], ['fa fa-share-square', '<i aria-hidden="true" class="fa fa-share-square"></i>'], ['fa fa-share-square-o', '<i aria-hidden="true" class="fa fa-share-square-o"></i>'], ['fa fa-shield', '<i aria-hidden="true" class="fa fa-shield"></i>'], ['fa fa-ship', '<i aria-hidden="true" class="fa fa-ship"></i>'], ['fa fa-shopping-bag', '<i aria-hidden="true" class="fa fa-shopping-bag"></i>'], ['fa fa-shopping-basket', '<i aria-hidden="true" class="fa fa-shopping-basket"></i>'], ['fa fa-shopping-cart', '<i aria-hidden="true" class="fa fa-shopping-cart"></i>'], ['fa fa-shower', '<i aria-hidden="true" class="fa fa-shower"></i>'], ['fa fa-sign-in', '<i aria-hidden="true" class="fa fa-sign-in"></i>'], ['fa fa-sign-language', '<i aria-hidden="true" class="fa fa-sign-language"></i>'], ['fa fa-sign-out', '<i aria-hidden="true" class="fa fa-sign-out"></i>'], ['fa fa-signal', '<i aria-hidden="true" class="fa fa-signal"></i>'], ['fa fa-signing', '<i aria-hidden="true" class="fa fa-signing"></i>'], ['fa fa-sitemap', '<i aria-hidden="true" class="fa fa-sitemap"></i>'], ['fa fa-sliders', '<i aria-hidden="true" class="fa fa-sliders"></i>'], ['fa fa-smile-o', '<i aria-hidden="true" class="fa fa-smile-o"></i>'], ['fa fa-snowflake-o', '<i aria-hidden="true" class="fa fa-snowflake-o"></i>'], ['fa fa-soccer-ball-o', '<i aria-hidden="true" class="fa fa-soccer-ball-o"></i>'], ['fa fa-sort', '<i aria-hidden="true" class="fa fa-sort"></i>'], ['fa fa-sort-alpha-asc', '<i aria-hidden="true" class="fa fa-sort-alpha-asc"></i>'], ['fa fa-sort-alpha-desc', '<i aria-hidden="true" class="fa fa-sort-alpha-desc"></i>'], ['fa fa-sort-amount-asc', '<i aria-hidden="true" class="fa fa-sort-amount-asc"></i>'], ['fa fa-sort-amount-desc', '<i aria-hidden="true" class="fa fa-sort-amount-desc"></i>'], ['fa fa-sort-asc', '<i aria-hidden="true" class="fa fa-sort-asc"></i>'], ['fa fa-sort-desc', '<i aria-hidden="true" class="fa fa-sort-desc"></i>'], ['fa fa-sort-down', '<i aria-hidden="true" class="fa fa-sort-down"></i>'], ['fa fa-sort-numeric-asc', '<i aria-hidden="true" class="fa fa-sort-numeric-asc"></i>'], ['fa fa-sort-numeric-desc', '<i aria-hidden="true" class="fa fa-sort-numeric-desc"></i>'], ['fa fa-sort-up', '<i aria-hidden="true" class="fa fa-sort-up"></i>'], ['fa fa-space-shuttle', '<i aria-hidden="true" class="fa fa-space-shuttle"></i>'], ['fa fa-spinner', '<i aria-hidden="true" class="fa fa-spinner"></i>'], ['fa fa-spoon', '<i aria-hidden="true" class="fa fa-spoon"></i>'], ['fa fa-square', '<i aria-hidden="true" class="fa fa-square"></i>'], ['fa fa-square-o', '<i aria-hidden="true" class="fa fa-square-o"></i>'], ['fa fa-star', '<i aria-hidden="true" class="fa fa-star"></i>'], ['fa fa-star-half', '<i aria-hidden="true" class="fa fa-star-half"></i>'], ['fa fa-star-half-empty', '<i aria-hidden="true" class="fa fa-star-half-empty"></i>'], ['fa fa-star-half-full', '<i aria-hidden="true" class="fa fa-star-half-full"></i>'], ['fa fa-star-half-o', '<i aria-hidden="true" class="fa fa-star-half-o"></i>'], ['fa fa-star-o', '<i aria-hidden="true" class="fa fa-star-o"></i>'], ['fa fa-sticky-note', '<i aria-hidden="true" class="fa fa-sticky-note"></i>'], ['fa fa-sticky-note-o', '<i aria-hidden="true" class="fa fa-sticky-note-o"></i>'], ['fa fa-street-view', '<i aria-hidden="true" class="fa fa-street-view"></i>'], ['fa fa-suitcase', '<i aria-hidden="true" class="fa fa-suitcase"></i>'], ['fa fa-sun-o', '<i aria-hidden="true" class="fa fa-sun-o"></i>'], ['fa fa-support', '<i aria-hidden="true" class="fa fa-support"></i>'], ['fa fa-tablet', '<i aria-hidden="true" class="fa fa-tablet"></i>'], ['fa fa-tachometer', '<i aria-hidden="true" class="fa fa-tachometer"></i>'], ['fa fa-tag', '<i aria-hidden="true" class="fa fa-tag"></i>'], ['fa fa-tags', '<i aria-hidden="true" class="fa fa-tags"></i>'], ['fa fa-tasks', '<i aria-hidden="true" class="fa fa-tasks"></i>'], ['fa fa-taxi', '<i aria-hidden="true" class="fa fa-taxi"></i>'], ['fa fa-television', '<i aria-hidden="true" class="fa fa-television"></i>'], ['fa fa-terminal', '<i aria-hidden="true" class="fa fa-terminal"></i>'], ['fa fa-thermometer', '<i aria-hidden="true" class="fa fa-thermometer"></i>'], ['fa fa-thermometer-0', '<i aria-hidden="true" class="fa fa-thermometer-0"></i>'], ['fa fa-thermometer-1', '<i aria-hidden="true" class="fa fa-thermometer-1"></i>'], ['fa fa-thermometer-2', '<i aria-hidden="true" class="fa fa-thermometer-2"></i>'], ['fa fa-thermometer-3', '<i aria-hidden="true" class="fa fa-thermometer-3"></i>'], ['fa fa-thermometer-4', '<i aria-hidden="true" class="fa fa-thermometer-4"></i>'], ['fa fa-thermometer-empty', '<i aria-hidden="true" class="fa fa-thermometer-empty"></i>'], ['fa fa-thermometer-full', '<i aria-hidden="true" class="fa fa-thermometer-full"></i>'], ['fa fa-thermometer-half', '<i aria-hidden="true" class="fa fa-thermometer-half"></i>'], ['fa fa-thermometer-quarter', '<i aria-hidden="true" class="fa fa-thermometer-quarter"></i>'], ['fa fa-thermometer-three-quarters', '<i aria-hidden="true" class="fa fa-thermometer-three-quarters"></i>'], ['fa fa-thumb-tack', '<i aria-hidden="true" class="fa fa-thumb-tack"></i>'], ['fa fa-thumbs-down', '<i aria-hidden="true" class="fa fa-thumbs-down"></i>'], ['fa fa-thumbs-o-down', '<i aria-hidden="true" class="fa fa-thumbs-o-down"></i>'], ['fa fa-thumbs-o-up', '<i aria-hidden="true" class="fa fa-thumbs-o-up"></i>'], ['fa fa-thumbs-up', '<i aria-hidden="true" class="fa fa-thumbs-up"></i>'], ['fa fa-ticket', '<i aria-hidden="true" class="fa fa-ticket"></i>'], ['fa fa-times', '<i aria-hidden="true" class="fa fa-times"></i>'], ['fa fa-times-circle', '<i aria-hidden="true" class="fa fa-times-circle"></i>'], ['fa fa-times-circle-o', '<i aria-hidden="true" class="fa fa-times-circle-o"></i>'], ['fa fa-times-rectangle', '<i aria-hidden="true" class="fa fa-times-rectangle"></i>'], ['fa fa-times-rectangle-o', '<i aria-hidden="true" class="fa fa-times-rectangle-o"></i>'], ['fa fa-tint', '<i aria-hidden="true" class="fa fa-tint"></i>'], ['fa fa-toggle-down', '<i aria-hidden="true" class="fa fa-toggle-down"></i>'], ['fa fa-toggle-left', '<i aria-hidden="true" class="fa fa-toggle-left"></i>'], ['fa fa-toggle-off', '<i aria-hidden="true" class="fa fa-toggle-off"></i>'], ['fa fa-toggle-on', '<i aria-hidden="true" class="fa fa-toggle-on"></i>'], ['fa fa-toggle-right', '<i aria-hidden="true" class="fa fa-toggle-right"></i>'], ['fa fa-toggle-up', '<i aria-hidden="true" class="fa fa-toggle-up"></i>'], ['fa fa-trademark', '<i aria-hidden="true" class="fa fa-trademark"></i>'], ['fa fa-trash', '<i aria-hidden="true" class="fa fa-trash"></i>'], ['fa fa-trash-o', '<i aria-hidden="true" class="fa fa-trash-o"></i>'], ['fa fa-tree', '<i aria-hidden="true" class="fa fa-tree"></i>'], ['fa fa-trophy', '<i aria-hidden="true" class="fa fa-trophy"></i>'], ['fa fa-truck', '<i aria-hidden="true" class="fa fa-truck"></i>'], ['fa fa-tty', '<i aria-hidden="true" class="fa fa-tty"></i>'], ['fa fa-tv', '<i aria-hidden="true" class="fa fa-tv"></i>'], ['fa fa-umbrella', '<i aria-hidden="true" class="fa fa-umbrella"></i>'], ['fa fa-universal-access', '<i aria-hidden="true" class="fa fa-universal-access"></i>'], ['fa fa-university', '<i aria-hidden="true" class="fa fa-university"></i>'], ['fa fa-unlock', '<i aria-hidden="true" class="fa fa-unlock"></i>'], ['fa fa-unlock-alt', '<i aria-hidden="true" class="fa fa-unlock-alt"></i>'], ['fa fa-unsorted', '<i aria-hidden="true" class="fa fa-unsorted"></i>'], ['fa fa-upload', '<i aria-hidden="true" class="fa fa-upload"></i>'], ['fa fa-user', '<i aria-hidden="true" class="fa fa-user"></i>'], ['fa fa-user-circle', '<i aria-hidden="true" class="fa fa-user-circle"></i>'], ['fa fa-user-circle-o', '<i aria-hidden="true" class="fa fa-user-circle-o"></i>'], ['fa fa-user-o', '<i aria-hidden="true" class="fa fa-user-o"></i>'], ['fa fa-user-plus', '<i aria-hidden="true" class="fa fa-user-plus"></i>'], ['fa fa-user-secret', '<i aria-hidden="true" class="fa fa-user-secret"></i>'], ['fa fa-user-times', '<i aria-hidden="true" class="fa fa-user-times"></i>'], ['fa fa-users', '<i aria-hidden="true" class="fa fa-users"></i>'], ['fa fa-vcard', '<i aria-hidden="true" class="fa fa-vcard"></i>'], ['fa fa-vcard-o', '<i aria-hidden="true" class="fa fa-vcard-o"></i>'], ['fa fa-video-camera', '<i aria-hidden="true" class="fa fa-video-camera"></i>'], ['fa fa-volume-control-phone', '<i aria-hidden="true" class="fa fa-volume-control-phone"></i>'], ['fa fa-volume-down', '<i aria-hidden="true" class="fa fa-volume-down"></i>'], ['fa fa-volume-off', '<i aria-hidden="true" class="fa fa-volume-off"></i>'], ['fa fa-volume-up', '<i aria-hidden="true" class="fa fa-volume-up"></i>'], ['fa fa-warning', '<i aria-hidden="true" class="fa fa-warning"></i>'], ['fa fa-wheelchair', '<i aria-hidden="true" class="fa fa-wheelchair"></i>'], ['fa fa-wheelchair-alt', '<i aria-hidden="true" class="fa fa-wheelchair-alt"></i>'], ['fa fa-wifi', '<i aria-hidden="true" class="fa fa-wifi"></i>'], ['fa fa-window-close', '<i aria-hidden="true" class="fa fa-window-close"></i>'], ['fa fa-window-close-o', '<i aria-hidden="true" class="fa fa-window-close-o"></i>'], ['fa fa-window-maximize', '<i aria-hidden="true" class="fa fa-window-maximize"></i>'], ['fa fa-window-minimize', '<i aria-hidden="true" class="fa fa-window-minimize"></i>'], ['fa fa-window-restore', '<i aria-hidden="true" class="fa fa-window-restore"></i>'], ['fa fa-wrench', '<i aria-hidden="true" class="fa fa-wrench"></i>']]

class Menu(forms.ModelForm):
    class Meta:
        model = models.Menu
        fields = '__all__'
        # exclude = ['permissions',]

        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'weight':forms.TextInput(attrs={'class':'form-control'}),
            # 'icon':forms.TextInput(attrs={'class':'form-control'}),
            'icon': forms.RadioSelect(choices=[[i[0], mark_safe(i[1])] for i in icon_list]),
        }



def menu_list(request):
    menus_id = request.GET.get('mid')
    obj= models.Menu.objects.all()

    if menus_id:
        permission_list = models.Permission.objects.filter(Q(menus_id=menus_id) | Q(parents__menus_id=menus_id)).values(
            'id', 'title', 'url', 'parents_id', 'reverse_name', 'menus__id',
            'menus__name', 'menus__icon')


    else:
        permission_list = models.Permission.objects.all().values('id', 'title', 'url', 'parents_id', 'reverse_name',
            'menus__id','menus__name', 'menus__icon')

    print('permission_list',permission_list)

    '''


    id  title  menus_id  parent_id
    1   客户展示  1        none
    2   客户添加  none     1
    3   客户编辑  none     1

    id  title  menus_id  parent_id
    1   客户展示  1        none
    2   客户添加  none     1
    3   客户编辑  none     1

    '''

    # print(permission_list)
    permission_dict = {}
    for permission in permission_list:
        pid = permission.get('menus__id')
        if pid:
            permission_dict[permission.get('id')] = permission
            permission_dict[permission.get('id')]['children'] = []
        # else:
        #     continue
    # print(permission_dict)

    for p in permission_list:
        parents_id = p.get('parents_id')
        if parents_id:  # 1
            permission_dict[parents_id]['children'].append(p)
        # else:
        #     continue

    print('permission_dict',permission_dict)
    '''
    {
        pid:{
             'title':'角色展示',
             'url':xx

            'children':[

            ]

        },
        pid:{
             'title':'角色展示',
             'url':xx

            'children':[
                {'title':'角色添加',}
            ]

        }

    }

    '''

    # print('>>>',permission_dict.values())

    return render(request, 'menu_list.html',
                  {'obj': obj, 'permission_list': permission_dict.values(), 'menus_id': menus_id})





def menu_add_edit(request,n=None):
    obj = models.Menu.objects.filter(pk=n).first()
    if request.method=='GET':
        obj1=Menu(instance=obj)
        return render(request,'menu_add_edit.html',{'obj':obj1})
    else:
        # print('request.post',request.post)
        # print('request.post',request.POST)
        obj1 = Menu(request.POST, instance=obj)
        if obj1.is_valid():
            obj1.save()
            return redirect('menu_list')
        else:
            return render(request,'menu_add_edit.html',{'obj':obj})

def menu_del(request,n):
    models.Menu.objects.filter(pk=n).delete()
    return redirect('menu_list')


def multi_permissions(request):
    """
    批量操作权限
    :param request:
    :return:
    """

    post_type = request.GET.get('type')  # add

    # 更新和编辑用的
    FormSet = modelformset_factory(models.Permission, MultiPermissionForm, extra=0)
    # 增加用的
    AddFormSet = formset_factory(MultiPermissionForm, extra=0)
    # FormSet(queyset=)
    # 查询数据库所有权限
    permissions = models.Permission.objects.all()

    # 获取路由系统中所有URL
    router_dict = get_all_url_dict(ignore_namespace_list=['admin', ])
    # url_ordered_dict['web:role_list'] = {'name': 'web:role_list', 'url': '/role/list/'}
    '''
    router_dict = {
        'web:role_list':{'name': 'web:role_list', 'url': '/role/list/'},
    }
    '''
    # 数据库中的所有权限的别名
    permissions_name_set = set([i.reverse_name for i in permissions])

    # 路由系统中的所有权限的别名
    router_name_set = set(router_dict.keys())

    if request.method == 'POST' and post_type == 'add':
        add_formset = AddFormSet(request.POST)
        if add_formset.is_valid():
            print(add_formset.cleaned_data)

            permission_obj_list = [models.Permission(**i) for i in add_formset.cleaned_data]

            query_list = models.Permission.objects.bulk_create(permission_obj_list)

            for i in query_list:
                permissions_name_set.add(i.reverse_name)

    add_name_set = router_name_set - permissions_name_set  # 新增的url别名信息

    add_formset = AddFormSet(initial=[row for name, row in router_dict.items() \
                                      if name in add_name_set])
    print('>>>>>>>>>>',
          [row for name, row in router_dict.items() \
           if name in add_name_set]
          )
    '''
    [{
            'name': 'web:login',
            'url': '/login/'
        }, {
            'name': 'web:index',
            'url': '/index/'
        }, {
            'name': 'rbac:menu_list',
            'url': '/rbac/menu/list/'
        }, {
            'name': 'rbac:menu_add',
            'url': '/rbac/menu/add/'
        }, {
            'name': 'rbac:menu_edit',
            'url': '/rbac/menu/edit/(\\d+)/'
        }, {
            'name': 'rbac:menu_del',
            'url': '/rbac/menu/del/(\\d+)/'
        }, {
            'name': 'rbac:multi_permissions',
            'url': '/rbac/multi/permissions/'
        }, {
            'name': 'xx',
            'url': '/xx'
        }]

    '''
    del_name_set = permissions_name_set - router_name_set  # 要删除的url别名信息
    del_formset = FormSet(queryset=models.Permission.objects.filter(reverse_name__in=del_name_set))
    # if request.method == 'POST' and post_type == 'delete':
    #     print(request.POST)

    update_name_set = permissions_name_set & router_name_set
    update_formset = FormSet(queryset=models.Permission.objects.filter(reverse_name__in=update_name_set))

    if request.method == 'POST' and post_type == 'update':
        update_formset = FormSet(request.POST)
        if update_formset.is_valid():
            update_formset.save()

            update_formset = FormSet(queryset=models.Permission. \
                                     objects.filter(reverse_name__in=update_name_set))

    return render(
        request,
        'multi_permissions.html',
        {
            'del_formset': del_formset,
            'update_formset': update_formset,
            'add_formset': add_formset,
        }
    )


def distribute_permissions(request):
    """
    分配权限
    :param request:
    :return:
    """
    uid = request.GET.get('uid')
    rid = request.GET.get('rid')

    if request.method == 'POST' and request.POST.get('postType') == 'role':
        user = models.UserInfo.objects.filter(id=uid).first()
        if not user:
            return HttpResponse('用户不存在')
        user.roles.set(request.POST.getlist('roles'))

    if request.method == 'POST' and request.POST.get('postType') == 'permission' and rid:
        role = models.Role.objects.filter(id=rid).first()
        if not role:
            return HttpResponse('角色不存在')
        role.permissions.set(request.POST.getlist('permissions'))

    # 所有用户
    user_list = models.UserInfo.objects.all()          # user列表
    user_has_roles = models.UserInfo.objects.filter(id=uid).values('id', 'roles')  # 获取用户user的职位与id
    # 类似字典{'id':'','roles':['','']}
    # username = models.CharField(max_length=32)
    # password = models.CharField(max_length=32)
    # roles = models.ManyToManyField('Role')

    print(user_has_roles)

    user_has_roles_dict = {item['roles']: None for item in user_has_roles}

    """
    用户拥有的角色id
    user_has_roles_dict = { 角色id：None }
    """

    role_list = models.Role.objects.all()    # 获取全部职位对象

    if rid:
        role_has_permissions = models.Role.objects.filter(id=rid).values('id', 'permissions')
        # 获取该职位的id及权限列表
    elif uid and not rid:
        user = models.UserInfo.objects.filter(id=uid).first()
        if not user:
            return HttpResponse('用户不存在')
        role_has_permissions = user.roles.values('id', 'permissions')
    else:
        role_has_permissions = []

    print(role_has_permissions)

    role_has_permissions_dict = {item['permissions']: None for item in role_has_permissions}

    """
    角色拥有的权限id
    role_has_permissions_dict = { 权限id：None }
    """

    all_menu_list = []

    queryset = models.Menu.objects.values('id', 'name')
    menu_dict = {}

    """

    all_menu_list = [
            {  id:   title :  , children : [
                { 'id', 'title', 'menus_id', 'children: [
                'id', 'title', 'parents_id'
                ]  }
            ] },
            {'id': None, 'title': '其他', 'children': [
            {'id', 'title', 'parents_id'}]}
    ]

    menu_dict = {
        菜单的ID： {  id:   title :  , children : [
            { 'id', 'title', 'menus_id', 'children: [
            'id', 'title', 'parents_id'
            ]  }
        ] },
        none:{'id': None, 'title': '其他', 'children': [
        {'id', 'title', 'parents_id'}]}
    }
    """

    for item in queryset:
        item['children'] = []  # 放二级菜单，父权限
        menu_dict[item['id']] = item
        all_menu_list.append(item)

    other = {'id': None, 'title': '其他', 'children': []}
    all_menu_list.append(other)
    menu_dict[None] = other

    root_permission = models.Permission.objects.filter(menus__isnull=False).values('id', 'title', 'menus_id')

    root_permission_dict = {}

    """
    root_permission_dict = { 父权限的id ： { 'id', 'title', 'menus_id', 'children: [
        { 'id', 'title', 'parents_id' }
    ]  }}
    """

    for per in root_permission:
        per['children'] = []  # 放子权限
        nid = per['id']
        menus_id = per['menus_id']
        root_permission_dict[nid] = per
        menu_dict[menus_id]['children'].append(per)

    node_permission = models.Permission.objects.filter(menus__isnull=True).values('id', 'title', 'parents_id')

    for per in node_permission:
        pid = per['parents_id']
        if not pid:
            menu_dict[None]['children'].append(per)
            continue
        root_permission_dict[pid]['children'].append(per)

    return render(
        request,
        'distribute_permissions.html',
        {
            'user_list': user_list,
            'role_list': role_list,
            'user_has_roles_dict': user_has_roles_dict,
            'role_has_permissions_dict': role_has_permissions_dict,
            'all_menu_list': all_menu_list,
            'uid': uid,
            'rid': rid
        }
    )





def distribute_permissions2(request):
    """
    分配权限
    :param request:
    :return:
    """
    uid = request.GET.get('uid')
    user = models.UserInfo.objects.filter(id=uid)
    rid = request.GET.get('rid')

    if request.method == "POST" and request.POST.get('postType') == 'role':
        print(request.POST.getlist("roles"))
        l = request.POST.getlist("roles")
        user.first().roles.set(l)

    # 所有用户
    user_list = models.UserInfo.objects.all()
    user_has_roles = user.values('id', 'roles')
    role_list = models.Role.objects.all()

    print("uid", uid)
    if uid:
        role_id_list = models.UserInfo.objects.get(pk=uid).roles.all().values_list("pk")
        role_id_list = [item[0] for item in role_id_list]
        per_id_list = models.UserInfo.objects.get(pk=uid).roles.values_list("permissions__pk").distinct()
        per_id_list = [item[0] for item in per_id_list]
        print("per_id_list", per_id_list)

    return render(request, 'distribute_permissions2.html', locals())





def permissions_tree(request):
    permissions = Permission.objects.values("pk", "title", "url", 'reverse_name',"menus__name", "menus__pk", "parents_id")
    print("permissions", permissions)

    return JsonResponse(list(permissions), safe=False)






