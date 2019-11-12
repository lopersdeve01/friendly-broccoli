from django.db import models

# Create your models here.

class Role(models.Model):
    name=models.CharField('职位名称',max_length=64,unique=True)
    permissions=models.ManyToManyField('Permission',verbose_name='权限')

    def __str__(self):
        return self.name


class UserInfo(models.Model):
    username=models.CharField('用户名',max_length=64,unique=True,null=True)
    password=models.CharField('密码',max_length=64)
    email=models.EmailField('邮箱',max_length=64,null=True,blank=True)
    telephone=models.IntegerField('电话号码',null=True,blank=True)
    roles=models.ManyToManyField(Role,verbose_name='职位',default=2)
    def __str__(self):
        return self.username
    # class Meta:
    #     abstract = True  # 这句就是当执行数据库同步指令的时候，这个类不生成表





class Menu(models.Model):
    name=models.CharField('一级菜单名称',max_length=64,unique=True)
    icon = models.CharField(max_length=150, null=True, blank=True)
    weight=models.IntegerField('权重')
    def __str__(self):
        return self.name







class Permission(models.Model):
    title=models.CharField('二级菜单名称',max_length=64,unique=True)
    url=models.CharField('路径',max_length=64,unique=True)
    reverse_name=models.CharField('别名',max_length=64,unique=True)
    menus=models.ForeignKey('Menu',verbose_name='一级菜单',null=True,blank=True)
    parents=models.ForeignKey('self',verbose_name='父级菜单',null=True,blank=True)
    def __str__(self):
        return self.title

#
# class Permission(models.Model):
#     title = models.CharField(max_length=32)
#     url = models.CharField(max_length=32)
#     menus = models.ForeignKey('Menu',null=True,blank=True)
#     parent = models.ForeignKey('self',null=True,blank=True)
#     url_name = models.CharField(max_length=32,null=True,blank=True)
#     # menu = models.BooleanField(default=False)
#     # icon = models.CharField(max_length=32,null=True,blank=True)
#
#     def __str__(self):
#         return self.title


