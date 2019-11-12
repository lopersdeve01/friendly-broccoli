from django.db import models

class Customer(models.Model):
    """
    客户表
    """
    name = models.CharField(verbose_name='姓名', max_length=32)
    age = models.CharField(verbose_name='年龄', max_length=32)
    email = models.EmailField(verbose_name='邮箱', max_length=32)
    company = models.CharField(verbose_name='公司', max_length=32)
    delete_status = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Payment(models.Model):
    """
    付费记录
    """
    customer = models.ForeignKey(verbose_name='关联客户', to='Customer')
    money = models.IntegerField(verbose_name='付费金额')
    create_time = models.DateTimeField(verbose_name='付费时间', auto_now_add=True)


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
    icon = models.CharField(max_length=150, null=True, blank=True)
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




    # parent = models.ForeignKey('self',null=True,blank=True)
    # url_name = models.CharField(max_length=32,null=True,blank=True)




