# from django.conf.urls import url
# from web import views
# # from web.views import payment
# # from web.views import auths
#
#
# urlpatterns = [
#     # 菜单权限展示表
#     # url(r'^customer/list/$', views.customer_list,name='customer_list'),
#     url(r'^menu/list/$', views.Menu.as_view(), name='menu_list'),
#     url(r'^menu/add/$', views.menu_add_edit,name='menu_add'),
#     # url(r'^customer/edit/(?P<cid>\d+)/$', views.customer_add_edit,name='customer_edit'),
#     url(r'^menu/edit/(\d+)/$', views.menu_add_edit, name='menu_edit'),
#     # url(r'^customer/del/(?P<cid>\d+)/$',views.customer_del,name='customer_del'),
#     url(r'^menu/del/(\d+)/$', views.menu_del, name='menu_del'),
#
#
#     # 职能展示表
#
#     url(r'^role/list/$', views.Role.as_view(), name='role_list'),
#     url(r'^role/add/$', views.role_add_edit,name='role_add'),
#
#     url(r'^role/edit/(\d+)/$', views.role_add_edit, name='role_edit'),
#
#     url(r'^role/del/(\d+)/$', views.role_del, name='role_del'),