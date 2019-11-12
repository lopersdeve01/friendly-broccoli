from django.db import models

# Create your models here.

class Tag(models.Model):
   """
   标签分类
   """
   title = models.CharField(verbose_name="标签",max_length=32)
   tid = models.IntegerField(verbose_name="标签ID",unique=True)

class Article(models.Model):
   """
   文章详情表
   """
   status = (
      (1,"发布"),
      (2,"删除"),
   )
   title = models.CharField(verbose_name="标题",max_length=128)
   create_at = models.DateTimeField(verbose_name="创建时间",auto_now_add=True)
   check = models.IntegerField(verbose_name="浏览数量")
   content = models.TextField(verbose_name="文章内容")
   photo = models.ImageField(verbose_name="文章图片",upload_to=None)
   article_status = models.IntegerField(verbose_name="文章状态",choices=status,default=1)
   tag = models.ForeignKey(verbose_name="关联标签",to="Tag",to_field="tid")

class Comment(models.Model):
   """
   文章评论
   """
   content = models.TextField(verbose_name="评论内容")
   content_time = models.DateTimeField(verbose_name="评论时间",auto_now_add=True)
   zan = models.IntegerField(verbose_name="点赞数")
   Article = models.ForeignKey(verbose_name="关联文章",to="Article")
