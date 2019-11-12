


from django.conf.urls import url
from django.contrib import admin
from rbac import views

from django.conf.urls import url,include
from rbac import views

app_name = 'rbac'
urlpatterns = [

    # 登陆
    url(r'^$', views.query, name='base'),
    url(r'^login/$', views.login, name='login'),
    url(r'^index/$', views.index, name='index'),


    # /app01/role/list/    # rbac:role_list
    url(r'^role/list/$', views.role_list, name='role_list'),
    url(r'^role/add/$', views.role, name='role_add'),
    url(r'^role/edit/(\d+)/$', views.role, name='role_edit'),
    url(r'^role/del/(\d+)/$', views.del_role, name='role_del'),

    url(r'^menu/list/$', views.menu_list, name='menu_list'),
    url(r'^menu/add/$', views.menu, name='menu_add'),
    url(r'^menu/edit/(\d+)/$', views.menu, name='menu_edit'),
    url(r'^menu/del/(\d+)/$', views.del_menu, name='menu_del'),

    url(r'^permission/add/$', views.permission, name='permission_add'),
    url(r'^permission/edit/(\d+)/$', views.permission, name='permission_edit'),
    url(r'^permission/del/(\d+)/$', views.del_permission, name='permission_del'),

    url(r'^multi/permissions/$', views.multi_permissions, name='multi_permissions'),

    url(r'^distribute/permissions/$', views.distribute_permissions, name='distribute_permissions'),
    url(r'^distribute/permissions2/$', views.distribute_permissions2, name='distribute_permissions'),
    url(r'^permissions_tree/$', views.permissions_tree, name='permissions_tree'),

]
