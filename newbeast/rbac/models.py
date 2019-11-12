from django.db import models

# Create your models here.

# 用户表
class UserInfo(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    roles = models.ManyToManyField('Role')
    def __str__(self):
        return self.username

# 角色表
class Role(models.Model):
    name = models.CharField(max_length=16)
    permissions = models.ManyToManyField('Permission')

    def __str__(self):
        return self.name


#  一级标题
class Menu(models.Model):
    name = models.CharField(max_length=32)
    icon = models.CharField(max_length=32, null=True, blank=True)
    weight = models.IntegerField(default=100)

    def __str__(self):
        return self.name


# 二级标题
class Permission(models.Model):
    title = models.CharField(max_length=32)
    url = models.CharField(max_length=32)
    menus = models.ForeignKey('Menu',null=True,blank=True)
    parents=models.ForeignKey('self',null=True,blank=True)
    reverse_name=models.CharField(max_length=32,null=True,blank=True)
    # icon = models.CharField(max_length=32,null=True,blank=True)

    def __str__(self):
        return self.title



