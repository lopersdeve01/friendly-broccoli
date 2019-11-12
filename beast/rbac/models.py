# from django.db import models
#
# # Create your models here.
#
# # 用户表
# class UserInfo(models.Model):
#     username = models.CharField(max_length=32)
#     password = models.CharField(max_length=32)
#     roles = models.ManyToManyField('Role')
#     def __str__(self):
#         return self.username
#
#
# # 角色表
# class Role(models.Model):
#     name = models.CharField(max_length=16)
#     permissions = models.ManyToManyField('Permission')
#
#     def __str__(self):
#         return self.name
#
#
# # 权限
# class Permission(models.Model):
#     title = models.CharField(max_length=32)
#     url = models.CharField(max_length=32)
#     menu = models.BooleanField(default=False)
#     # icon = models.CharField(max_length=32,null=True,blank=True)
#
#     def __str__(self):
#         return self.title



