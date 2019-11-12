from django.db import models

# Create your models here.
class Userinfo(models.Model):
    username=models.CharField(verbose_name="username",max_length=32)
    password=models.CharField(verbose_name='password',max_length=32)


class Blog(models.Model):
    title=models.CharField(verbose_name='title',max_length=32)
    content=models.TextField(verbose_name='content')
    author=models.ForeignKey(verbose_name='author',to='Userinfo')


