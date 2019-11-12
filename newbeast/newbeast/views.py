from django.shortcuts import render
from django.shortcuts import HttpResponse,redirect,render
from django import forms
import copy
from django.db.models import Q
import os
import mimetypes
from django.shortcuts import render, redirect
from django.http import FileResponse
from django.conf import settings
from web import models
from web.forms.customer import CustomerForm
from django.views import View
from web.page import Page
from collections import OrderedDict











def index(request):

    return render(request,'index.html')

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
        #     # print(menu_dict)
        #     request.session['menu_dict']=menu_dict

        if obj :
            request.session['is_login']=True
            request.session['username']= username
            ret=models.Role.objects.filter(userinfo__username=username).values('permissions__pk','permissions__url','permissions__title',
            'permissions__parents_id','permissions__reverse_name','permissions__menus__pk',
            'permissions__menus__name', 'permissions__menus__icon','permissions__menus__weight').distinct()
            request.session['ret']=list(ret)
            print(ret)
            reverse_names = []                                   #  别名集合
            permission_dict = {}
            menu_data = {}
            for i in ret:
                permission_dict[i.get('permissions__pk')] = i        #二级菜单字典
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
                                {'title': i.get('permissions__title'), 'url': i.get('permissions__url'),
                                 'parents_id': i.get('permissions__parents_id'),
                                 'reverse_name': i.get('permissions__reverse_name')},
                            ],
                        }


            # print('menu_data',menu_data)

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
            request.session['menu_dict'] = menu_dict
            # request.session['bread_crumb']=
            # 根绝列表中字典间的顺序，对字典的进行排序，形成有序字典，并封装到session中
            # print(menu_data)
            # print('permission_dict',permission_dict)
            # print('reverse_names', reverse_names)
            # print('menu_dict', menu_dict)    # 权重排序字典
            return redirect('index')
        else:
            return redirect('/login/')