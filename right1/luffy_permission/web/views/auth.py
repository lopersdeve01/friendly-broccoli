
from django.shortcuts import HttpResponse,redirect,render
from rbac import models
from rbac.utils.permission_injection import init_permission
def login(request):

    if request.method == 'GET':
        return render(request,'login.html')
    else:
        uname = request.POST.get('username')
        pwd = request.POST.get('password')

        user_obj = models.UserInfo.objects.filter(username=uname,password=pwd)
        if user_obj:
            user_obj = user_obj.first()
            # 登录认证标识
            request.session['is_login'] = True

            # 权限注入
            init_permission(request,user_obj)

            # 1 权限表设计(model)
            # 2 权限分配(数据分配)
            # 3 查询权限并注入权限(封装的session功能)
            # 4 权限验证(中间件)
            # 5 动态生成左侧菜单




            # 登录成功之后，将该用户所有的权限(url)全部注入到session中
            # permission_list = models.Role.objects.filter(userinfo__username=user_obj.username)\
            #     .values('permissions__url','permissions__title','permissions__menu','permissions__icon').distinct()
            # request.session['permission_list'] = list(permission_list)  # Object of type 'QuerySet' is not JSON serializable
            #
            # # 筛选菜单权限
            # menu_list = []
            # for permission in permission_list:
            #     if permission.get('permissions__menu'):
            #         menu_list.append(permission)
            # # 将菜单权限注入到session
            # request.session['menu_list'] = menu_list

            # print(menu_list)
            # models.UserInfo.objects.filter(username=user_obj.username).values('roles__permissons__url')
            # models.Permission.objects.filter(role__userinfo__username=user_obj.username).values('url')
            # print(permission_list)
            # [{'permissons__url': '/customer/list/'},
            # {'permissons__url': '/customer/add/'},
            # {'permissons__url': '/customer/edit/(?P<cid>\\d+)/'},
            # {'permissons__url': '/customer/del/(?P<cid>\\d+)/'},
            # {'permissons__url': '/payment/list/'},
            # {'permissons__url': '/customer/list/'}]

            return redirect('index')


        else:
            return redirect('login')


def index(request):

    return render(request,'index.html')

