from django.db import models

# Create your models here.


class Category(models.Model):
    """
    文章分类
    """
    name = models.CharField(verbose_name='分类',max_length=32)
    def __str__(self):
        return self.name


class Article(models.Model):
    """
    文章表
    """
    status_choices=(
        (1,'发布'),
        (2,'删除'),
    )
    title = models.CharField(verbose_name='标题',max_length=32)
    summary = models.CharField(verbose_name='简介',max_length=255)
    content = models.TextField(verbose_name='文章内容')
    categorys=models.ForeignKey('Category',verbose_name='类型')
    status=models.IntegerField(verbose_name='状态',choices=status_choices,default=1)
    tags=models.ManyToManyField(to='Tag',verbose_name='标签')

class Tag(models.Model):
    title=models.CharField(verbose_name='标签',max_length=32)
    def __str__(self):
        return self.title
