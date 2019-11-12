from django.urls import reverse
from django.utils.safestring import mark_safe
from django import template
from django.http.request import QueryDict
from django.conf import settings
import re

register = template.Library()

# @register.filter
@register.inclusion_tag('menu.html')
def menu(request):
    # menu_list =  request.session.get('menu_list')
    # print(menu_list)
    # for i in menu_list:
    #     if i.get('permissions__url') == request.path:
    #         i['class'] = 'active'
    # # print(111)
    # # print(menu_list)
    # # print(222)
    # # [{'permissions__url': '/customer/list/', 'permissions__title': '客户管理', 'permissions__menu': True, 'permissions__icon': 'fa fa-camera'}]
    # menu_data = {'menu_data':menu_list}
    # return menu_data
    menu_dict=request.session.get('menu_dict')
    print('menu_dict>>>>>>>>>>>>>>',menu_dict)
    # for k,v in menu_dict.items():
    #     v['class'] = 'hidden'    # 字典的值默认为隐藏，即子标签默认为隐藏，为以后点击释放做准备
    #     # 子菜单与目菜单
    #     #  OrderedDict([(1, {'name': '登陆系统', 'icon': None, 'weight': 100, 'children': [{'title': '登陆', 'url': '/login/'}]}), (2, {'name': '业务系统', 'icon': None, 'weight': 90, 'children': [{'title': '展示客户', 'url': '/customer/list/'}]})])
    #     for i in v['children']:
    #         if re.match(i['url'],request.path):
    #             i['class'] = 'active'       # 访问路径与子标签匹配，如果成功，添加active属性，hidden属性更改为‘’（不再隐藏），否则该父标签仍为hidden属性
    #             v['class']=''               #

        # else:
        #     pass

    # for i in menu_dict:
    #     if i.get('permissions__url') == request.path:
    #         i['class'] = 'active'
    # {'1': {'name': None, 'icon': None, 'weight': 100,
    #        'children': [{'title': '系统登录', 'url': '/login/', 'parents_id': None, 'reverse_name': None},
    #                     {'title': '首页', 'url': '/index/', 'parents_id': 5, 'reverse_name': None, 'class': 'active'}],
    #        'class': ''},
    # '2': {'name': None, 'icon': None, 'weight': 90, 'children': [
    #     {'title': '客户管理', 'url': '/customer/list/', 'parents_id': None, 'reverse_name': None},
    #     {'title': '添加客户', 'url': '/customer/add/', 'parents_id': 1, 'reverse_name': None},
    #     {'title': '编辑客户', 'url': '/customer/edit/', 'parents_id': 1, 'reverse_name': None},
    #     {'title': '删除客户', 'url': '/customer/del/(?P<cid>\\d+)/', 'parents_id': 1, 'reverse_name': None}],
    #                            'class': 'hidden'}}
    for k, v in menu_dict.items():
        # print('menu_dict',v)
        # print('request',request)
        # print('request.parent_id',request.parent_id)
        v['class'] = 'hidden'  # 字典的值默认为隐藏，即子标签默认为隐藏，为以后点击释放做准备
        # 子菜单与目菜单
        path=request.path
        # print('path',path)
        #  OrderedDict([(1, {'name': '登陆系统', 'icon': None, 'weight': 100, 'children': [{'title': '登陆', 'url': '/login/'}]}), (2, {'name': '业务系统', 'icon': None, 'weight': 90, 'children': [{'title': '展示客户', 'url': '/customer/list/'}]})])
        for i in v['children']:
            print('request.pid', request.pid)
            print('i.get(permissions__pk)', i.get('pk'))
            # print('i.get(permissions__pk)',i.get(permissions__pk))
            # if i.get('parents_id')==i.get('permissions__pk'):
            if request.pid==i.get('pk'):
                print(request.pid==i.get('pk'))
                # if re.match(i['url'], request.path):
                i['class'] = 'active'  # 访问路径与子标签匹配，如果成功，添加active属性，hidden属性更改为‘’（不再隐藏），否则该父标签仍为hidden属性
                v['class'] = ''  #
                break
            else:
                continue
            # else:


    # print(menu_dict)
    # [{'permissions__url': '/customer/list/', 'permissions__title': '客户管理', 'permissions__menu': True, 'permissions__icon': 'fa fa-camera'}]
    # menu_data = {'menu_data':menu_dict}
    menu_data = {'menu_dict':menu_dict}
    return menu_data


@register.simple_tag
def reverse_url(url_name,id,request):

    # /editcustomer/3/?next=/customers/?page=4
    path = request.get_full_path()
    query_dict_obj = QueryDict(mutable=True)
    query_dict_obj['next'] = path #
    encode_url = query_dict_obj.urlencode() #next=/customers/?search_field=qq__contains&keyword=1&page=4
    # url编码:
    #next=%2Fcustomers%2F%3Fsearch_field%3Dqq__contains%26keyword%3D1%26page%3D4
    #next=%2Fcustomers%2F%3Fsearch_field%3Dqq__contains%26keyword%3D1%26page%3D4


    # ?a=1&b=2
    # request.GET = queryDict({'a':1,'b':2})
    # request.GET.urlencode() -- a=1&b=2

    #queryDict({'next':'/customers/?search_field=qq__contains&keyword=1&page=4'})


     #/customers/?page=4  #/customers/?search_field=qq__contains&keyword=1&page=4
    prefix_path = reverse(url_name,args=(id,)) #/editcustomer/3/

    full_path = prefix_path + '?' + encode_url
    print(full_path)

    return full_path
# print(type(request.GET)) #<class 'django.http.request.QueryDict'> request.GET.urlencode()
##http://127.0.0.1:8000/editcustomer/116/?next=/customers/?search_field=qq__contains&keyword=1&page=4

# 跳转回的路径:  http://127.0.0.1:8000/customers/?search_field=qq__contains&keyword=1&page=4


# @register.inclusion_tag('href.html')
# def edit_del(url_name,id,request):
#     # path=request.get_full_path()
#     # pre_fix=reverse('url_name',args=(id,))
#     # request.post.get('next')
#
#     path = request.get_full_path()
#     query_dict_obj = QueryDict(mutable=True)
#     query_dict_obj['next'] = path #
#     encode_url = query_dict_obj.urlencode() #next=/customers/?search_field=qq__contains&keyword=1&page=4
#
#     prefix_path = reverse(url_name, args=(id,))
#     full_path=prefix_path+'?'+encode_url
#     print(111)
#     print(full_path)
#     print(222)
#     return full_path
#



@register.filter
def has_permission(request, permission):
    if permission in request.session.get(settings.PERMISSION_SESSION_KEY):
        return True


@register.simple_tag
def gen_role_url(request, rid):
    params = request.GET.copy()
    params._mutable = True
    params['rid'] = rid
    return params.urlencode()



