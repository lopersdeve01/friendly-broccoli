from django.conf.urls import url
from web import views
# from web.views import payment
# from web.views import auth


urlpatterns = [
    # 登陆
    url(r'^$', views.query, name='base'),
    url(r'^login/$', views.login, name='login'),
    url(r'^index/$', views.index, name='index'),

    # 客户展示
    # url(r'^customer/list/$', views.customer_list,name='customer_list'),
    # url(r'^customer/list/$', views.Customers.as_view(), name='customer_list'),
    # url(r'^customer/add/$', views.customer_add_edit,name='customer_add'),
    # # url(r'^customer/edit/(?P<cid>\d+)/$', views.customer_add_edit,name='customer_edit'),
    # url(r'^customer/edit/(\d+)/$', views.customer_add_edit, name='customer_edit'),
    # # url(r'^customer/del/(?P<cid>\d+)/$',views.customer_del,name='customer_del'),
    # url(r'^customer/del/(\d+)/$', views.customer_del, name='customer_del'),


    # url(r'^customer/edita/(\d+)/$', views.edit_del, name='customer_edita'),
    # url(r'^customer/delete/(\d+)/$', views.edit_del, name='customer_delete'),



    # 菜单管理
    url(r'^menu/list/', views.menu_list, name='menu_list'),
    url(r'^menu/add/', views.menu_add_edit, name='menu_add'),
    url(r'^menu/edit/(\d+)/', views.menu_add_edit, name='menu_edit'),
    url(r'^menu/del/(\d+)/', views.menu_del, name='menu_del'),


    # 角色展示
    url(r'^role/list/', views.role_list, name='role_list'),  # /rbac/customer/
    url(r'^role/add/', views.role_add_edit, name='role_add'),  # /rbac/customer/
    url(r'^role/edit/(\d+)/', views.role_add_edit, name='role_edit'),  # /rbac/customer/
    url(r'^role/del/(\d+)/', views.role_del, name='role_del'),  # /rbac/customer/
    # url(r'^recb', include('rebc.urls')),

    # 批量操作权限
    url(r'^multi/permissions/$', views.multi_permissions, name='multi_permissions'),


    #  人事职位权限管理
    url(r'^distribute/permissions/$', views.distribute_permissions, name='distribute_permissions'),
    url(r'^distribute/permissions2/$', views.distribute_permissions2, name='distribute_permissions'),
    url(r'^permissions_tree/$', views.permissions_tree, name='permissions_tree'),

    ]
