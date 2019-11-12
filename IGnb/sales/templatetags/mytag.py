
from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def show_info(request):
    path = request.path
    if path == reverse('sales:customers'):
        return mark_safe('<option value="reverse_gs">公户转私户</option>')
    else:
        return mark_safe('<option value="reverse_sg">私户转公户</option>')

# 拼接路径,编辑之后跳转回原页面
@register.simple_tag
def reverse_url(url_name,id,request):
    from django.http.request import QueryDict
    path = request.get_full_path()
    query_dict_obj = QueryDict(mutable=True)
    query_dict_obj['next'] = path
    encode_url = query_dict_obj.urlencode()
    prefix_path = reverse(url_name,args=(id,))
    full_path = prefix_path + '?' +  encode_url
    return full_path
