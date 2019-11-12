from django.db import models

# Create your models here.

# 一级菜单数据表
class Menu(models.Model):
    name = models.CharField(max_length=32)

    weight = models.IntegerField(default=100)  #控制菜单排序的,权重值越大,菜单展示越靠前
    icon = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.name

'''
    一级菜单
    id  name  icon
    1   业务系统  
    2   教务系统
    
    
    权限表
    id   title  url                  menu_id
    1    客户展示 /list/               1
    2    客户添加 /add/               None
    3    跟进记录展示 /plist/           1
    4    课程记录  /course/             2
    5    课程记录添加    /add/course/  None
    
'''



# 权限
class Permission(models.Model):
    title = models.CharField(max_length=32)
    url = models.CharField(max_length=32)
    menus = models.ForeignKey('Menu',null=True,blank=True)
    parent = models.ForeignKey('self',null=True,blank=True)
    url_name = models.CharField(max_length=32,null=True,blank=True)
    # menu = models.BooleanField(default=False)
    # icon = models.CharField(max_length=32,null=True,blank=True)

    def __str__(self):
        return self.title

class Role(models.Model):
    name = models.CharField(max_length=16)
    permissions = models.ManyToManyField('Permission')

    def __str__(self):
        return self.name

# models.Permission.objects.filter(parent__menus_id=mid)
# 用户表
class UserInfo(models.Model):
    # username = models.CharField(max_length=32)
    # password = models.CharField(max_length=32)
    roles = models.ManyToManyField(Role)
    # def __str__(self):
    #     return self.username
    class Meta:
        abstract = True  # 这句就是当执行数据库同步指令的时候，这个类不生成表

# import sys
# f = sys.modules[__name__]
# getattr(f,'Role')












