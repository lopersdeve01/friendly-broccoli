from django.contrib import admin

# Register your models here.


from app01 import models

# class UserInfoAdmin(admin.ModelAdmin):
#     # list_display = ['username','email','telephone']
#     # list_editable = ['username','email','telephone']

admin.site.register(models.Blog)
admin.site.register(models.Article)
# admin.site.register(models.UserInfo,UserInfoAdmin)
admin.site.register(models.UserInfo)





# class Blog(models.Model):
#     name=models.CharField('博客名称',max_length=64,unique=True)
#     # user=models.CharField('用户名',max_length=64,unique=True)
#     users=models.OneToOneField('UserInfo',verbose_name='用户名')
#     def __str__(self):
#         return self.name
#
#
# class Article(models.Model):
#     category_choices=(
#     (1,'未分类'),
#     (2,'技术'),
#     (3,'杂谈'),
#     (4,'感悟'),
#     )
#     title=models.CharField('文章标题',max_length=128,unique=True)
#     category=models.IntegerField('文章分类',choices=category_choices,default=1)
#     blog=models.ForeignKey('Blog',verbose_name='所属博客')
#     content=models.TextField('文章内容')
#     create_at=models.DateTimeField(auto_now_add=True,blank=True)
#     def __str__(self):
#         return self.title
#
#
# class UserInfo(models.Model):
#     username=models.CharField('用户名',max_length=64,unique=True)
#     password=models.CharField('密码',max_length=64)
#     email=models.EmailField('邮箱',max_length=64)
#     telephone=models.IntegerField('电话号码',max_length=11)
#     def __str__(self):
#         return self.username
