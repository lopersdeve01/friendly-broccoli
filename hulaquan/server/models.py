from django.db import models

# Create your models here.

# class Category(models.Model):
#     """
#     文章分类
#     """
#     name = models.CharField(verbose_name='分类',max_length=32)
#     cid = models.IntegerField(verbose_name='分类值',unique=True)
#
#     def __str__(self):
#         return self.name
#
#     # category_choices = (
#     #     (1, '未分类'),
#     #     (2, '技术'),
#     #     c
#     #     (4, '感悟'),
#     # )

class Article(models.Model):
    """
    文章表
    """
    category_choices = (
        (1, '经验'),
        (2, '技术'),
        (3, '杂谈'),
        (4, '感悟'),
    )
    status_choices=(
        (1,'发布'),
        (2,'删除'),
    )
    title = models.CharField(verbose_name='标题',max_length=32)
    # summary = models.CharField(verbose_name='简介',max_length=255)
    imgs=models.CharField(verbose_name='图片',max_length=255)
    content = models.TextField(verbose_name='文章内容')
    # categorys=models.ForeignKey(to="Category",to_field="cid",verbose_name='分类',null=True,blank=True)
    category = models.IntegerField('文章分类', choices=category_choices, default=1)
    create_at = models.DateTimeField(auto_now_add=True, blank=True)
    status=models.IntegerField(verbose_name='状态',choices=status_choices,default=1)
    # tags=models.ManyToManyField(to='Tag',verbose_name='标签',null=True,blank=True)
    scan = models.IntegerField(verbose_name='阅读量',default=0)
    author=models.ForeignKey("User",verbose_name='作者')
    def __str__(self):
        return self.title

class ArticleDetails(models.Model):
    content=models.TextField(verbose_name='内容',default='请输入内容')
    articles=models.ForeignKey("Article",verbose_name="所属文章")
    def __str__(self):
        return self.articles.title



class Tag(models.Model):
    title=models.CharField(verbose_name='标签',max_length=32)
    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField(verbose_name='评论内容')
    create_at = models.DateTimeField(auto_now_add=True, blank=True)
    users=models.ForeignKey('User',verbose_name='用户')
    articles = models.ForeignKey('Article', verbose_name='所属文章')
    def __str__(self):
        return self.create_at

class User(models.Model):
    name=models.CharField(max_length=32,verbose_name='用户名')
    password=models.CharField(max_length=32,verbose_name='密码')
    token=models.CharField(verbose_name='token',max_length=64)
    roles=models.ForeignKey('Role',verbose_name='身份')
    def __str__(self):
        return self.name

class Img(models.Model):
    name=models.CharField(max_length=32,verbose_name='图片名称')
    url=models.ImageField(max_length=255,verbose_name='图片路径')
    articles = models.ForeignKey('Article', verbose_name='所属文章')
    def __str__(self):
        return self.name
class Role(models.Model):
    name=models.CharField(verbose_name='身份',max_length=32)
    permissions=models.ManyToManyField('Permission',verbose_name='权限')


class Permission(models.Model):
    name = models.CharField(max_length=32, verbose_name='权限名')
    url= models.CharField(max_length=32, verbose_name='路径')
    url_name=models.CharField(max_length=64, verbose_name='别名')
    def __str__(self):
        return self.name


