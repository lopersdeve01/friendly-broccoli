from django.contrib import admin

# Register your models here.

from rbac import models
# class AdminiAdmin(admin.ModelAdmin):
#     list_display = ['email','telephone']
#     list_editable = ['email','telephone']
#
# class PermissionAdmin(admin.ModelAdmin):
#     list_display = [ 'url', 'url_name']
#     list_editable = ['url', 'url_name']

# admin.site.register(models.Admini,AdminiAdmin)
# admin.site.register(models.Admini)
admin.site.register(models.Role)
admin.site.register(models.Menu)
admin.site.register(models.UserInfo)#
# admin.site.register(models.Permission,PermissionAdmin)
admin.site.register(models.Permission)

# class Admini(models.Model):
    # username = models.CharField('用户名', max_length=64, unique=True)
    # password = models.CharField('密码', max_length=64)
    # email = models.EmailField('邮箱', max_length=64)
    # telephone = models.IntegerField('电话号码', max_length=11)
    #
    #
    # def __str__(self):
    #     return self.username
#
#
# class Role(models.Model):
#     title = models.CharField('职位名称', max_length=64, unique=True)
#     permissions = models.ManyToManyField('Permission', verbose_name='权限')
#
#     def __str__(self):
#         return self.title
#
#
# class Menu(models.Model):
#     name = models.CharField('一级菜单名称', max_length=64, unique=True)
#     weight = models.IntegerField('权重')
#
#     def __str__(self):
#         return self.name
#
#
# class Permission(models.Model):
#     name = models.CharField('二级菜单名称', max_length=64, unique=True)
#     url = models.CharField('路径', max_length=64, unique=True)
#     url_name = models.CharField('别名', max_length=64, unique=True)
#     menus = models.ForeignKey('Menu', verbose_name='一级菜单')
#     parents = models.ForeignKey('self', verbose_name='父级菜单')
#
#     def __str__(self):
#         return self.name



# username:debug
# password:debug123