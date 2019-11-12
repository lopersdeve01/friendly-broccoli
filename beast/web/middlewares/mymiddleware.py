import re

from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.shortcuts import redirect,HttpResponse,render
# 'web.middlewares.mymiddleware.Auth',
class Auth(MiddlewareMixin):

    def process_request(self,request):
        # 登录认证白名单
        white_list = [reverse('login'),]
        # 权限认证白名单
        permission_white_list = [reverse('index'), '/admin/*','/favicon.ico']#/admin/login/?next=/admin/  # 加上'',用于通过127.0.0.1:8000
        # WHITE_URL_LIST = [
        #     r'/login/$',
        #     r'^/logout/$',
        #     r'^/reg/$',
        #     r'^/admin/.*',
        # ]



        request.pid = None

        bread_crumb = [
            {'url': reverse('index'), 'title': '首页'},
            # {'url': reverse('login'), 'title': '登陆'},
            # {'url': reverse('customer_list'), 'title': '客户管理'},
            # {'url': reverse('customer_add'), 'title': '添加客户'},
            # {'url': reverse('customer_list'), 'title': '客户管理'},
            # {'url': reverse('customer_add'), 'title': '添加客户'},
            # # {'url': reverse('customer_edit'), 'title': '编辑管理'},
            # {'url': reverse('customer_del'), 'title': '删除客户'},
        ]
        # print('type',type(request))

        request.bread_crumb = bread_crumb

        # 登录认证
        path = request.path
        if path not in white_list:
            is_login = request.session.get('is_login')
            if not is_login:
                return redirect('login')
            # 权限认证
            ret = request.session.get('ret')

            # [{'permissions__url': '/customer/list/'},
            # {'permissions__url': '/customer/add/'},
            # {'permissions__url': '/customer/edit/(?P<cid>\\d+)/'},
            # {'permissions__url': '/customer/del/(?P<cid>\\d+)/'},
            # {'permissions__url': '/payment/list/'},
            # {'permissions__url': '/customer/list/'}]
            # /customer/edit/5/
            # if path not in permission_white_list:
            permission_dict = request.session.get('permission_dict')
            for request_path in permission_white_list:
                if re.match(request_path,path):
                    break
                print(11)

                print('permission_dict',permission_dict)
            else:
                print(22)
                print('permission_dict.values()',permission_dict.values())
                for i in permission_dict.values():

                    # print('i[permissions__url]',i['permissions__url'])

                    reg = r"^%s$"%(i['permissions__url'])
                    # print('full_path',request.get_full_path())
                    print(reg,path)
                    # print('path',path)
                    # a=re.match(reg,path)
                    # print('匹配结果',a)
                    if re.match(reg,path):
                        print(33)
                        pid = i.get('permissions__parents_id')  ##path  = /payment/add/  -- 5
                        print('pid',pid)
                        # menu_data
                        # {2: {'pk': 1, 'name': '业务系统', 'icon': None, 'weight': 90, 'children': [
                        #     {'title': '客户管理', 'url': '/customer/list/', 'parents_id': None,
                        #      'reverse_name': 'customer_list'},
                        #     {'title': '添加客户', 'url': '/customer/add/', 'parents_id': 1, 'reverse_name': 'customer_add'},
                        #     {'title': '编辑客户', 'url': '/customer/edit/', 'parents_id': 1,
                        #      'reverse_name': 'customer_edit'},
                        #     {'title': '删除客户', 'url': '/customer/del/(?P<cid>\\d+)/', 'parents_id': 1,
                        #      'reverse_name': 'customer_del'}]},
                        #  1: {'pk': 5, 'name': '登陆系统', 'icon': None, 'weight': 100, 'children': [
                        #      {'title': '系统登录', 'url': '/login/', 'parents_id': None, 'reverse_name': 'login'},
                        #      {'title': '首页', 'url': '/index/', 'parents_id': 5, 'reverse_name': 'index'}]}}



                        # permission_dict
                        # {1: {'permissions__pk': 1, 'permissions__url': '/customer/list/', 'permissions__title': '客户管理',
                        #      'permissions__parents_id': None, 'permissions__reverse_name': 'customer_list',
                        #      'permissions__menus__pk': 2, 'permissions__menus__name': '业务系统',
                        #      'permissions__menus__icon': None, 'permissions__menus__weight': 90},
                        #  2: {'permissions__pk': 2, 'permissions__url': '/customer/add/', 'permissions__title': '添加客户',
                        #      'permissions__parents_id': 1, 'permissions__reverse_name': 'customer_add',
                        #      'permissions__menus__pk': 2, 'permissions__menus__name': '业务系统',
                        #      'permissions__menus__icon': None, 'permissions__menus__weight': 90},
                        #  3: {'permissions__pk': 3, 'permissions__url': '/customer/edit/', 'permissions__title': '编辑客户',
                        #      'permissions__parents_id': 1, 'permissions__reverse_name': 'customer_edit',
                        #      'permissions__menus__pk': 2, 'permissions__menus__name': '业务系统',
                        #      'permissions__menus__icon': None, 'permissions__menus__weight': 90},
                        #  4: {'permissions__pk': 4, 'permissions__url': '/customer/del/(?P<cid>\\d+)/',
                        #      'permissions__title': '删除客户', 'permissions__parents_id': 1,
                        #      'permissions__reverse_name': 'customer_del', 'permissions__menus__pk': 2,
                        #      'permissions__menus__name': '业务系统', 'permissions__menus__icon': None,
                        #      'permissions__menus__weight': 90},
                         # 5: {'permissions__pk': 5, 'permissions__url': '/login/', 'permissions__title': '系统登录',
                         #     'permissions__parents_id': None, 'permissions__reverse_name': 'login',
                         #     'permissions__menus__pk': 1, 'permissions__menus__name': '登陆系统',
                         #     'permissions__menus__icon': None, 'permissions__menus__weight': 100},
                         # 6: {'permissions__pk': 6, 'permissions__url': '/index/', 'permissions__title': '首页',
                         #     'permissions__parents_id': 5, 'permissions__reverse_name': 'index',
                         #     'permissions__menus__pk': 1, 'permissions__menus__name': '登陆系统',
                             # 'permissions__menus__icon': None, 'permissions__menus__weight': 100}}
                        # reverse_names[None, None, None, None, None, None]
                        # menu_dict
                        # OrderedDict([(1, {'pk': 5, 'name': '登陆系统', 'icon': None, 'weight': 100, 'children': [
                        #     {'title': '系统登录', 'url': '/login/', 'parents_id': None, 'reverse_name': 'login'},
                        #     {'title': '首页', 'url': '/index/', 'parents_id': 5, 'reverse_name': 'index'}]}), (2,
                     # {'pk': 1,
                     #  'name': '业务系统',
                     #  'icon': None,
                     #  'weight': 90,
                     #  'children': [
                     #      {
                     #          'title': '客户管理',
                     #          'url': '/customer/list/',
                     #          'parents_id': None,
                     #          'reverse_name': 'customer_list'},
                     #      {
                     #          'title': '添加客户',
                     #          'url': '/customer/add/',
                     #          'parents_id': 1,
                     #          'reverse_name': 'customer_add'},
                     #      {
                     #          'title': '编辑客户',
                     #          'url': '/customer/edit/',
                     #          'parents_id': 1,
                     #          'reverse_name': 'customer_edit'},
                     #      {
                     #          'title': '删除客户',
                     #          'url': '/customer/del/(?P<cid>\\d+)/',
                     #          'parents_id': 1,
                     #          'reverse_name': 'customer_del'}]})])
                        if pid:  #
                            print(44)

                            # parent_permission = models.Permission.objects.get(pk=pid)
                            # 父级二级菜单路径信息
                            request.bread_crumb.append(
                                {'url': permission_dict[str(pid)]['permissions__url'],  # KeyError
                                 'title': permission_dict[str(pid)]['permissions__title'], }
                            )

                            # 子权限的路径信息  #/payment/add/
                            request.bread_crumb.append(
                                {'url': i.get('permissions__url'), 'title': i.get('permissions__title')}
                            )
                            request.pid = pid
                            print('request.bread_crumb', request.bread_crumb)
                            print('request.pid',request.pid)

                        else:
                            print(55)
                            # 二级菜单路径信息
                            request.bread_crumb.append(
                                {'url': i.get('permissions__url'), 'title': i.get('permissions__title')}
                            )
                            request.pid = i.get('permissions__pk')

                            print('request.bread_crumb', request.bread_crumb)
                            print('request.pid', request.pid)
                        break

                    #     # break
                    # else:
                    #     continue

                else:
                    return HttpResponse('权限不足！')










