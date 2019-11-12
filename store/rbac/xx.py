# permissions_list = {1:{
# 	'permissions__url': '/customer/list/',
# 	'permissions__pk': 1,
# 	'permissions__title': '客户管理',
# 	'permissions__menus__pk': 1,
# 	'permissions__menus__name': '业务系统',
# 	'permissions__menus__icon': 'fa fa-home fa-fw',
# 	'permissions__menus__weight': 100,
# 	'permissions__parent_id': None
# }, 2:{
# 	'permissions__url': '/customer/add/',
# 	'permissions__pk': 2,
# 	'permissions__title': '添加客户',
# 	'permissions__menus__pk': None,
# 	'permissions__menus__name': None,
# 	'permissions__menus__icon': None,
# 	'permissions__menus__weight': None,
# 	'permissions__parent_id': 1
# },3: {
# 	'permissions__url': '/customer/edit/(?P<cid>\\d+)/',
# 	'permissions__pk': 3,
# 	'permissions__title': '编辑客户',
# 	'permissions__menus__pk': None,
# 	'permissions__menus__name': None,
# 	'permissions__menus__icon': None,
# 	'permissions__menus__weight': None,
# 	'permissions__parent_id': 1
# },4: {
# 	'permissions__url': '/customer/del/(?P<cid>\\d+)/',
# 	'permissions__pk': 4,
# 	'permissions__title': '删除客户',
# 	'permissions__menus__pk': None,
# 	'permissions__menus__name': None,
# 	'permissions__menus__icon': None,
# 	'permissions__menus__weight': None,
# 	'permissions__parent_id': 1
# }, 5:{
# 	'permissions__url': '/payment/list/',
# 	'permissions__pk': 5,
# 	'permissions__title': '账单管理',
# 	'permissions__menus__pk': 2,
# 	'permissions__menus__name': '财务系统',
# 	'permissions__menus__icon': 'fa fa-jpy fa-fw',
# 	'permissions__menus__weight': 200,
# 	'permissions__parent_id': None
# }, 6:{
# 	'permissions__url': '/payment/add/',
# 	'permissions__pk': 6,
# 	'permissions__title': '添加缴费',
# 	'permissions__menus__pk': None,
# 	'permissions__menus__name': None,
# 	'permissions__menus__icon': None,
# 	'permissions__menus__weight': None,
# 	'permissions__parent_id': 5
# },7: {
# 	'permissions__url': '/payment/edit/(?P<pid>\\d+)/',
# 	'permissions__pk': 7,
# 	'permissions__title': '编辑缴费',
# 	'permissions__menus__pk': None,
# 	'permissions__menus__name': None,
# 	'permissions__menus__icon': None,
# 	'permissions__menus__weight': None,
# 	'permissions__parent_id': 5
# }, 8:{
# 	'permissions__url': '/payment/del/(?P<pid>\\d+)/',
# 	'permissions__pk': 8,
# 	'permissions__title': '删除缴费',
# 	'permissions__menus__pk': None,
# 	'permissions__menus__name': None,
# 	'permissions__menus__icon': None,
# 	'permissions__menus__weight': None,
# 	'permissions__parent_id': 5
# },9: {
# 	'permissions__url': '/nashui/',
# 	'permissions__pk': 9,
# 	'permissions__title': '纳税展示',
# 	'permissions__menus__pk': 2,
# 	'permissions__menus__name': '财务系统',
# 	'permissions__menus__icon': 'fa fa-jpy fa-fw',
# 	'permissions__menus__weight': 200,
# 	'permissions__parent_id': None
# }}
# #{1: {'permissions__url': '/customer/list/', 'permissions__pk': 1, 'permissions__title': '客户管理', 'permissions__menus__pk': 1, 'permissions__menus__name': '业务系统', 'permissions__menus__icon': 'fa fa-home fa-fw', 'permissions__menus__weight': 100, 'permissions__parent_id': None, 'permissions__url_name': 'customer_list'}, 2: {'permissions__url': '/customer/add/', 'permissions__pk': 2, 'permissions__title': '添加客户', 'permissions__menus__pk': None, 'permissions__menus__name': None, 'permissions__menus__icon': None, 'permissions__menus__weight': None, 'permissions__parent_id': 1, 'permissions__url_name': 'customer_add'}, 3: {'permissions__url': '/customer/edit/(?P<cid>\\d+)/', 'permissions__pk': 3, 'permissions__title': '编辑客户', 'permissions__menus__pk': None, 'permissions__menus__name': None, 'permissions__menus__icon': None, 'permissions__menus__weight': None, 'permissions__parent_id': 1, 'permissions__url_name': 'customer_edit'}, 4: {'permissions__url': '/customer/del/(?P<cid>\\d+)/', 'permissions__pk': 4, 'permissions__title': '删除客户', 'permissions__menus__pk': None, 'permissions__menus__name': None, 'permissions__menus__icon': None, 'permissions__menus__weight': None, 'permissions__parent_id': 1, 'permissions__url_name': 'customer_del'}, 5: {'permissions__url': '/payment/list/', 'permissions__pk': 5, 'permissions__title': '账单管理', 'permissions__menus__pk': 2, 'permissions__menus__name': '财务系统', 'permissions__menus__icon': 'fa fa-jpy fa-fw', 'permissions__menus__weight': 200, 'permissions__parent_id': None, 'permissions__url_name': 'payment_list'}}

# import sys

#
# def xx1():
#     a = {'1': [11, 22, 33]}
#
#     xx2(a)
#
#     print(a)
#
# def xx2(a):
#     a['1'].append('44')
#
# xx1()
#
# import json
#
# a = {1:'xx',2:2}
# s = json.dumps(a)
# print(s)
# print(json.loads(s))
# f = sys.modules[__name__]
#
# a = 11
#
# def xx():
#     print('xxx')
# print(f.a)
# print(f.xx())