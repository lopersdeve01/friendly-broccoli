from django.db import models

# Create your models here.
class UserInfo(models.Model):
    username=models.CharField(verbose_name="用户名",max_length=32)
    password=models.CharField(verbose_name='密码',max_length=64)
    def __str__(self):
        return self.username
class Article(models.Model):
    category_choices=((1,'资讯'),(2,'公司动态'),(3,'分享'),(4,'答疑'),(5,'其他'))
    category=models.IntegerField(verbose_name='分类',choices=category_choices)
    title=models.CharField(verbose_name='标题',max_length=32)
    image=models.CharField(verbose_name='图片路径',max_length=128)
    summary=models.CharField(verbose_name='简介',max_length=255)
    comment_count=models.IntegerField(verbose_name='评论数',default=0)
    read_count=models.IntegerField(verbose_name='浏览数',default=0)
    author=models.ForeignKey('UserInfo',verbose_name='作者')
    data=models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    def __str__(self):
        return self.title
class ArticleDetail(models.Model):
    article=models.OneToOneField('Article',verbose_name='文章')
    content=models.TextField(verbose_name='内容')
    def __str__(self):
        return self.article.title
class Comment(models.Model):
    article=models.ForeignKey('Article',verbose_name='文章')
    content=models.TextField(verbose_name='评论')
    user=models.ForeignKey('UserInfo',verbose_name='评论者')
    parent=models.ForeignKey('self',verbose_name='回复',null=True,blank=True)
    def __str__(self):
        return '%s:%s'%(self.article.title,self.user)


