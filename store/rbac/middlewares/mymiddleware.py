import re
from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.shortcuts import redirect,HttpResponse,render
from rbac import models


# from django.utils.deprecation import MiddlewareMixin
# from django.urls import reverse
# from django.shortcuts import redirect,HttpResponse,render
#
# class Auth(MiddlewareMixin):
#     white_list = [reverse('sales:login'),reverse('sales:register'),]
#     def process_request(self,request):
#         if request.path not in self.white_list:
#             username = request.session.get('username')
#             if not username:
#                 return redirect('sales:login')
#         print('the reuqest is coming!')
#     def process_response(self,request,response):
#         print('the request is far away!')
#         return response









class Auth(MiddlewareMixin):

    def process_request(self,request):
        # request.session
        # 登录认证白名单
        white_list = [reverse('sales:login'),reverse('sales:register')]
        # 权限认证白名单
        permission_white_list = [reverse('sales:home'), '/admin/*',] #/admin/login/?next=/admin/

        request.pid = None
        
        bread_crumb = [
            {'url':reverse('sales:home'),'title':'首页'},
            # {'url':'/index/','title':'首页1'},
            # {'url':'/index/','title':'首页2'},
        ]
        print(type(request))

        request.bread_crumb = bread_crumb

        # 登录认证
        path = request.path
        if path not in white_list:
            is_login = request.session.get('username')

            if not is_login:
                return redirect('sales:login')

        # 权限认证
            permission_dict = request.session.get('permission_dict') #{'1': 'xx', '2': 2}
            # print(permission_list)
            # [{'permissions__url': '/customer/list/'},
            # {'permissions__url': '/customer/add/'},
            # {'permissions__url': '/customer/edit/(?P<cid>\\d+)/'},
            # {'permissions__url': '/customer/del/(?P<cid>\\d+)/'},
            # {'permissions__url': '/payment/list/'},
            # {'permissions__url': '/customer/list/'}]
            # /customer/edit/5/
            # if path not in permission_white_list:
            for white_path in permission_white_list:
                if re.match(white_path,path):
                    break

            else:
                for i in permission_dict.values():
                    reg = r"^%s$"%i['permissions__url']
                    if re.match(reg,path): #path  = /payment/list/  -- None
                        pid = i.get('permissions__parent_id') ##path  = /payment/add/  -- 5


                        if pid: # 5

                            # parent_permission = models.Permission.objects.get(pk=pid)

                            # 父级二级菜单路径信息
                            request.bread_crumb.append(
                                {'url':permission_dict[str(pid)]['permissions__url'], #KeyError
                                 'title':permission_dict[str(pid)]['permissions__title'], }
                            )

                            # 子权限的路径信息  #/payment/add/
                            request.bread_crumb.append(
                                {'url': i.get('permissions__url'), 'title': i.get('permissions__title')}
                            )
                            request.pid = pid

                        else:
                            # 二级菜单路径信息
                            request.bread_crumb.append(
                                {'url':i.get('permissions__url'),'title':i.get('permissions__title')}
                            )
                            request.pid = i.get('permissions__pk')

                        break
                else:
                    return HttpResponse('权限不足？？！')

    def process_response(self, request, response):
        print('the request is far away!')
        return response







