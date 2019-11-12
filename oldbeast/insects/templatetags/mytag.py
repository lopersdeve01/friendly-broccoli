
from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.http.request import QueryDict

register = template.Library()

@register.simple_tag
def show_info(request):
    path = request.path
    if path == reverse('customer'):
        return mark_safe('<option value="reverse_gs">公户转私户</option>')
    else:
        return mark_safe('<option value="reverse_sg">私户转公户</option>')

# 拼接路径,编辑之后跳转回原页面
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

    full_path = prefix_path + '?' +  encode_url

    return full_path
# print(type(request.GET)) #<class 'django.http.request.QueryDict'> request.GET.urlencode()
##http://127.0.0.1:8000/editcustomer/116/?next=/customers/?search_field=qq__contains&keyword=1&page=4

# 跳转回的路径:  http://127.0.0.1:8000/customers/?search_field=qq__contains&keyword=1&page=4