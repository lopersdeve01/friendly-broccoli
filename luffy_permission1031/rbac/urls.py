from django.conf.urls import url,include
from rbac import views

urlpatterns = [
    # 角色管理
    url(r'^role/list/', views.role_list,name='role_list'),    #/rbac/customer/
    url(r'^role/add/', views.role_add_edit,name='role_add'),    #/rbac/customer/
    url(r'^role/edit/(\d+)/', views.role_add_edit,name='role_edit'),    #/rbac/customer/
    url(r'^role/del/(\d+)/', views.role_del,name='role_del'),    #/rbac/customer/
    # url(r'^recb', include('rebc.urls')),

    # 菜单管理
    url(r'^menu/list/', views.menu_list,name='menu_list'),
    url(r'^menu/add/', views.menu_add_edit,name='menu_add'),
    url(r'^menu/edit/(\d+)/', views.menu_add_edit,name='menu_edit'),
    url(r'^menu/del/(\d+)/', views.menu_del,name='menu_del'),

    # 批量操作权限
    url(r'^multi/permissions/$', views.multi_permissions, name='multi_permissions'),

]
