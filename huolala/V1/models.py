from django.db import models

# Create your models here.

class Article(models.Model):
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
    # imgs = models.ForeignKey('Img',verbose_name='图片')
    category = models.IntegerField('文章分类', choices=category_choices, default=1)
    create_at = models.DateTimeField(auto_now_add=True, blank=True)
    status= models.IntegerField(verbose_name='状态',choices=status_choices,default=1)
    scan = models.IntegerField(verbose_name='阅读量',default=0)
    author= models.ForeignKey("User",verbose_name='作者')
    comment_count=models.IntegerField(verbose_name='评论数')
    def __str__(self):
        return self.title

class Img(models.Model):
    name=models.CharField(max_length=32,verbose_name='图片名称')
    url=models.ImageField(max_length=255,verbose_name='图片路径',null=True,blank=True)
    articles = models.ManyToManyField('Article', verbose_name='所属文章')
    def __str__(self):
        return self.name

class ArticleDetails(models.Model):
    content=models.TextField(verbose_name='内容')
    articles=models.OneToOneField("Article",verbose_name="所属文章")
    def __str__(self):
        return self.articles.title

# class Tag(models.Model):
#     title=models.CharField(verbose_name='标签',max_length=32)
#     def __str__(self):
#         return self.title
class User(models.Model):
    name=models.CharField(max_length=32,verbose_name='用户名')
    password=models.CharField(max_length=32,verbose_name='密码')
    token=models.CharField(verbose_name='token',max_length=64,null=True,blank=True)
    roles=models.ForeignKey('Role',verbose_name='身份')
    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(verbose_name='身份', max_length=32)
    permissions = models.ManyToManyField('Permission', verbose_name='权限')
    def __str__(self):
        return self.name

class Permission(models.Model):
    name = models.CharField(max_length=32, verbose_name='权限名')
    url= models.CharField(max_length=32, verbose_name='路径',null=True,blank=True)
    url_name=models.CharField(max_length=64, verbose_name='别名',null=True,blank=True)
    def __str__(self):
        return self.name

class Comment(models.Model):
    content = models.TextField(verbose_name='评论内容',default=1)
    create_at = models.DateTimeField(auto_now_add=True, blank=True)
    users=models.ForeignKey('User',verbose_name='用户')

    # 标准的自关联字段
    parents=models.ForeignKey('self',verbose_name='回复',null=True,blank=True)

    articles = models.ForeignKey('Article', verbose_name='所属文章')
    def __str__(self):
        return "%s:%s"%(self.users.name,self.articles.title)





