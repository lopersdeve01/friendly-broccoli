from django.shortcuts import render,HttpResponse,render
from rbac import models
from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from django import forms
from app01 import models
from rbac.models import Permission, Role
from django.shortcuts import render, HttpResponse, redirect, reverse
from rbac import models
from rbac.forms import *
from django.db.models import Q
from rbac.server.routes import get_all_url_dict
import copy
from django.db.models import Q
from django.conf import settings
from django.views import View
from django.forms import modelformset_factory, formset_factory


from collections import OrderedDict
from app01.page import Page
from django.forms import modelformset_factory,formset_factory
from app01.routes import get_all_url_dict
from app01.forms.forms import MultiPermissionForm
from django.utils.safestring import mark_safe

from rbac.models import Permission,Role
from django.shortcuts import render, HttpResponse, redirect, reverse
from rbac import models
from rbac.forms import *
from django.db.models import Q
from rbac.server.routes import get_all_url_dict

# Create your views here.

def query(request):
    # obj_list=[]
    # lst='abcdefghijklmnopqrstuvwxyz'
    # for i in range(0,len(lst)):
    #     obj=models.UserInfo(
    #         name=lst[i]*3+'1',
    #         age = 24,
    #         email = lst[i]*3+'@qq.com',
    #         company =lst[i]+'.com',
    #         )
    #     obj_list.append(obj)
    # models.UserInfo.objects.bulk_create(obj_list)
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

            return redirect('rbac:index')
        else:
            return redirect('rbac:login')

def index(request):

    return render(request,'index.html')


def role_list(request):
    all_roles = models.Role.objects.all()
    return render(request, 'role_list.html', {"all_roles": all_roles})


def role(request, edit_id=None):
    obj = models.Role.objects.filter(id=edit_id).first()
    form_obj = RoleForm(instance=obj)
    if request.method == 'POST':
        form_obj = RoleForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('rbac:role_list'))

    return render(request, 'form.html', {'form_obj': form_obj})


def del_role(request, del_id):
    models.Role.objects.filter(id=del_id).delete()
    return redirect(reverse('rbac:role_list'))


# 菜单信息  权限信息
def menu_list(request):
    print(111)
    all_menu = models.Menu.objects.all()

    mid = request.GET.get('mid')
    print('mid',mid)

    if mid:
        permission_query = models.Permission.objects.filter(Q(menus_id=mid) | Q(parents__menus_id=mid))
    else:
        permission_query = models.Permission.objects.all()

    all_permission = permission_query.values('id', 'url', 'title', 'reverse_name', 'menus_id', 'parents_id', 'menus__name')
    print('all_permission',all_permission)

    all_permission_dict = {}

    for item in all_permission:
        # {
        #     'id': 1,
        #     'url': '/app01/blog/list/',
        #     'title': '博客展示',
        #     'reverse_name': 'blog_list',
        #     'menus_id': 1,
        #     'parents_id': None,
        #     'menus__name': '博客系统'
        # },
        menus_id = item.get('menus_id')
        if menus_id:
            item['children'] = []
            all_permission_dict[item['id']] = item
            # all_permission_dict{1：item}

    for item in all_permission:
        pid = item.get('parents_id')

        if pid:
            all_permission_dict[pid]['children'].append(item)

    print('all_permission_dict',all_permission_dict)
    print("all_menu", all_menu)

    return render(request, 'menu_list.html',{'all_menu': all_menu, 'all_permission_dict': all_permission_dict.values(), 'mid': mid})
    # return render(request, 'menu_list.html',{'obj': obj,           'permission_list': permission_dict.values(), 'menus_id': menus_id})

def menu(request, edit_id=None):
    obj = models.Menu.objects.filter(id=edit_id).first()
    form_obj = MenuForm(instance=obj)
    if request.method == 'POST':
        form_obj = MenuForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('rbac:menu_list'))

    return render(request, 'form.html', {'form_obj': form_obj})

def del_menu(request,n):
    models.Menu.objects.filter(pk=n).delete()
    return redirect('rbac:menu_del')


def permission(request, edit_id=None):
    obj = models.Permission.objects.filter(id=edit_id).first()
    form_obj = PermissionForm(instance=obj)
    if request.method == 'POST':
        form_obj = PermissionForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('rbac:menu_list'))

    return render(request, 'form.html', {'form_obj': form_obj})


def del_permission(request, del_id):
    models.Permission.objects.filter(id=del_id).delete()
    return redirect(reverse('rbac:menu_list'))




def multi_permissions(request):
    """
    批量操作权限
    :param request:
    :return:
    """

    post_type = request.GET.get('type')

    # 更新和编辑用的
    FormSet = modelformset_factory(models.Permission, MultiPermissionForm, extra=0)
    # 增加用的
    AddFormSet = formset_factory(MultiPermissionForm, extra=0)

    permissions = models.Permission.objects.all()

    # 获取路由系统中所有URL
    router_dict = get_all_url_dict(ignore_namespace_list=['admin'])
    print('router_dict',router_dict)

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
    print('permissions_name_set',permissions_name_set)
    print('router_name_set',router_name_set)
    add_name_set = router_name_set - permissions_name_set
    add_formset = AddFormSet(initial=[row for title, row in router_dict.items() if title in add_name_set])

    del_name_set = permissions_name_set - router_name_set
    del_formset = FormSet(queryset=models.Permission.objects.filter(reverse_name__in=del_name_set))

    update_name_set = permissions_name_set & router_name_set
    print('update_name_set',update_name_set)
    update_formset = FormSet(queryset=models.Permission.objects.filter(reverse_name__in=update_name_set))

    if request.method == 'POST' and post_type == 'update':
        update_formset = FormSet(request.POST)
        print('update_formset',update_formset)
        if update_formset.is_valid():
            update_formset.save()
            update_formset = FormSet(queryset=models.Permission.objects.filter(reverse_name__in=update_name_set))

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
    user_list = models.UserInfo.objects.all()
    user_has_roles = models.UserInfo.objects.filter(id=uid).values('id', 'roles')

    # print(user_has_roles)

    user_has_roles_dict = {item['roles']: None for item in user_has_roles}

    """
    用户拥有的角色id
    user_has_roles_dict = { 角色id：None }
    """

    role_list = models.Role.objects.all()
    print(role_list)

    if rid:
        role_has_permissions = models.Role.objects.filter(id=rid).values('id', 'permissions')
    elif uid and not rid:
        user = models.UserInfo.objects.filter(pk=uid).first()
        if not user:
            return HttpResponse('用户不存在')
        role_has_permissions = user.roles.values('pk','permissions')
        # user = models.UserInfo.objects.filter(id=uid).first()

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
                { 'id', 'title', 'menu_id', 'children: [
                'id', 'title', 'parent_id'
                ]  }
            ] },
            {'id': None, 'title': '其他', 'children': [
            {'id', 'title', 'parent_id'}]}
    ]

    menu_dict = {
        菜单的ID： {  id:   title :  , children : [
            { 'id', 'title', 'menu_id', 'children: [
            'id', 'title', 'parent_id'
            ]  }
        ] },
        none:{'id': None, 'title': '其他', 'children': [
        {'id', 'title', 'parent_id'}]}
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
    root_permission_dict = { 父权限的id ： { 'id', 'title', 'menu_id', 'children: [
        { 'id', 'title', 'parent_id' }
    ]  }}
    """

    for per in root_permission:
        per['children'] = []  # 放子权限
        nid = per['id']
        menus_id = per['menus_id']
        root_permission_dict[nid] = per
        menu_dict[menus_id]['children'].append(per)

    node_permission = models.Permission.objects.filter(menus__isnull=True).values('pk', 'title', 'parents_id')

    for per in node_permission:
        pid = per['parents_id']
        print('per',per)
        print('pid',pid)
        if not pid:
            menu_dict[None]['children'].append(per)
            # continue
        else:
            root_permission_dict[pid]['children'].append(per)
    print('root_permission_dict',root_permission_dict)
    print('all_menu_list',all_menu_list)

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


from django.http import JsonResponse


def permissions_tree(request):
    permissions = Permission.objects.values("pk", "title", "url", "menus__name", "menus__pk", "parents_id")
    print("permissions", permissions)

    return JsonResponse(list(permissions), safe=False)




