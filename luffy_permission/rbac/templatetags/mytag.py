

from django import template
import re
from collections import OrderedDict
register = template.Library()

# @register.filter
@register.inclusion_tag('menu.html')
def menu(request):
    # menu_list =  request.session.get('menu_list')
    menu_dict =  request.session.get('menu_dict')

    menu_order_key = sorted(menu_dict, key=lambda x: menu_dict[x]['weight'], reverse=True)

    # print(sort_d1)

    menu_order_dict = OrderedDict()

    for key in menu_order_key:
        menu_order_dict[key] = menu_dict[key]

    path = request.path
    for k,v in menu_order_dict.items():
        v['class'] = 'hidden'
        for i in v['children']:
            # /customer/add/
            # if re.match(i['url'],path):  # 获取当前访问路径对应的parent_id == i['permissions__pk']
            if request.pid == i['second_menu_id']:  #
                v['class'] = ''
                i['class'] = 'active'

        # else:
        #     pass

    # for i in menu_dict:
    #     if i.get('permissions__url') == request.path:
    #         i['class'] = 'active'

    print(menu_dict)
    # [{'permissions__url': '/customer/list/', 'permissions__title': '客户管理', 'permissions__menu': True, 'permissions__icon': 'fa fa-camera'}]
    # menu_data = {'menu_data':menu_dict}
    menu_data = {'menu_order_dict':menu_order_dict}
    return menu_data


@register.inclusion_tag('breadcrumb.html')
def bread_crumb(request):
    bread_crumb = request.bread_crumb
    data = {'bread_crumb':bread_crumb}
    return data



