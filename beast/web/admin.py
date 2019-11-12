from django.contrib import admin

# Register your models here.

from web import models


class MenuAdmin(admin.ModelAdmin):
    list_display=['name','weight']
    # list_editable=['name',]

class PermissionAdmin(admin.ModelAdmin):
    list_display = ['id','title','url','menus','reverse_name','parents']
    list_editable = ['title','url','menus','reverse_name','parents']

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['username',]

class RoleAdmin(admin.ModelAdmin):
    list_display = ['name',]
    # list_editable = ['title','url','menu','icon']

admin.site.register(models.UserInfo,UserInfoAdmin)
admin.site.register(models.Role,RoleAdmin)
admin.site.register(models.Menu,MenuAdmin)
admin.site.register(models.Permission,PermissionAdmin)
admin.site.register(models.Customer)
admin.site.register(models.Payment)
# username:beast
# password:beast123


#进行函数的插件筛选，首先要建立功能权限的列表，
# 通过将标签选中与否决定是否选用标签。get('menu')
# #其次将列表展示在网页的左侧边框中。
# 加上动态效果，包括显示激活状态。
# models.Permission.objects.filter(menu=True)
#当一个用户已经登陆，那么他的素有权限均已经展示在session中。那么控制权限使用的就是中间键
#相对与用户权限的标签展示，就会出现相当的
#拿到标签列表，if request.path==




















