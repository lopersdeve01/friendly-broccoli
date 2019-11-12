# from django.contrib import admin
#
# # Register your models here.
#
# from rbac import models
#
# class MenuAdmin(admin.ModelAdmin):
#     list_display=['name','weight']
#     # list_editable=['name',]
#
# class PermissionAdmin(admin.ModelAdmin):
#     list_display = ['id','title','url','menus','reverse_name','parents']
#     list_editable = ['title','url','menus','reverse_name','parents']
#
# class RoleAdmin(admin.ModelAdmin):
#     list_display = ['name',]
#     # list_editable = ['title','url','menu','icon']
#
#
#
# admin.site.register(models.Role,RoleAdmin)
# admin.site.register(models.Menu,MenuAdmin)
# admin.site.register(models.Permission,PermissionAdmin)
#
