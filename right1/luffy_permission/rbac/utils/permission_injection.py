
from rbac import models

# 权限注入到session中
def init_permission(request,user_obj):
    # 登录成功之后，将该用户所有的权限(url)全部注入到session中
    permission_list = models.Role.objects.filter(userinfo__username=user_obj.username) \
        .values('permissions__url',
                'permissions__pk',
                'permissions__title',
                'permissions__menus__pk',
                'permissions__menus__name',
                'permissions__menus__icon',
                'permissions__menus__weight',
                'permissions__parent_id',
                'permissions__url_name'
                ).distinct()
    # request.session['permission_list'] = list(permission_list)  # Object of type 'QuerySet' is not JSON serializable

    url_names = []

    permission_dict = {}

    # 菜单权限数据结构
    menu_dict = {}
    for i in permission_list:
        permission_dict[i.get('permissions__pk')] = i
        url_names.append(i.get('permissions__url_name'))
        if i.get('permissions__menus__pk'):
            if i.get('permissions__menus__pk') in menu_dict:
                menu_dict[i.get('permissions__menus__pk')]['children'].append(
                    {'title': i.get('permissions__title'),
                     'url': i.get('permissions__url'),
                     'second_menu_id': i.get('permissions__pk'),
                     }
                )
            else:
                menu_dict[i.get('permissions__menus__pk')] = {
                    'name':i.get('permissions__menus__name'),
                    'icon':i.get('permissions__menus__icon'),
                    'weight':i.get('permissions__menus__weight'),
                    'children':[
                        {'title':i.get('permissions__title'),
                         'url':i.get('permissions__url'),
                         'second_menu_id':i.get('permissions__pk'),  #
                         },

                    ],
                }
    # print(menu_dict)
    request.session['menu_dict'] = menu_dict
    request.session['url_names'] = url_names

    request.session['permission_dict'] = permission_dict
    print(permission_dict)
    # # 筛选菜单权限
    # menu_list = []
    # for permission in permission_list:
    #     if permission.get('permissions__menu'):
    #         menu_list.append(permission)
    # # 将菜单权限注入到session
    # request.session['menu_list'] = menu_list






