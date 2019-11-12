from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from django import forms
from app01 import models

import copy
from django.db.models import Q
from django.conf import settings
from django.views import View

from collections import OrderedDict
from app01.page import Page
from django.forms import modelformset_factory,formset_factory
from app01.routes import get_all_url_dict
from app01.forms.forms import MultiPermissionForm
from django.utils.safestring import mark_safe

# from rbac.models import Permission,Role




class Blog(forms.ModelForm):
    class Meta:
        model=models.Blog
        fields='__all__'
        labels={'name':'博客名称','users':'用户名'}

def blog_list(request):
    obj=models.Blog.objects.all()
    return render(request,'blog_list.html',{'obj':obj})


def blog_add_edit(request,n=None):
    if request.method == "GET":
        instance = models.Blog.objects.filter(pk=n).first()
        obj = Blog(instance=instance)
        print(obj)
        return render(request, 'blog_add_edit.html', {'obj': obj})
    else:
        next_path = request.GET.get('next')  #
        print(next_path)
        instance = models.Blog.objects.filter(pk=n).first()
        obj = Blog(request.POST, instance=instance)
        if obj.is_valid():
            obj.save()
            print(request.POST)
            print(obj)
            # return render(request,'blog_list.html', {'obj': obj})
            return redirect('app01:blog_list')
        else:
            return redirect(request.path)
def blog_del(request,n):
    models.Blog.objects.filter(pk=n).delete()
    # obj=models.Blog.objects.filter(delete_status=False)
    # return redirect(request.path)
    return redirect('app01:blog_list')




class Article(forms.ModelForm):
    class Meta:
        model=models.Article
        fields='__all__'
        labels={'title':'文章标题','category':'文章分类','blog':'所属博客','create_at':'创建时间'}

def article_list(request):
    obj=models.Article.objects.all()
    return render(request,'article_list.html',{'obj':obj})

def article_add_edit(request,n=None):
    obj = models.Article.objects.filter(pk=n).first()
    if request.method=='GET':
        obj1=Article(instance=obj)
        return render(request,'article_add_edit.html',{'obj':obj1})
    else:
        obj1=Article(request.POST,instance=obj)
        if obj1.is_valid():
            obj1.save()
            return redirect('app01:article_list')
        else:
            return render(request,'article_add_edit.html',{'obj':obj})

def article_del(request,n):
    models.Article.objects.filter(pk=n).delete()
    return redirect('app01:article_list')
