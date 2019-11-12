
from django.shortcuts import render, HttpResponse
from django.views import View
from django.http import JsonResponse
from hulaquan import models

from rest_framework.views import APIView
from rest_framework.response import Response
from django.forms.models import model_to_dict
from rest_framework import serializers
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView,GenericAPIView
from rest_framework.pagination import LimitOffsetPagination
from django.db.models import Count,F
from django.db import transaction
from rest_framework.versioning import URLPathVersioning





class PageArticleSerializer(serializers.ModelSerializer):
    comment_num = serializers.SerializerMethodField()
    summary = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    # check = serializers.SerializerMethodField()

    class Meta:
        model=models.Article
        fields='__all__'
        # fields = ['pk', 'title', 'create_at', 'summary', 'photo','check','comment_num','comments']
    def get_comment_num(self,obj):
        # print('obj',type(obj))
        # ret=models.Comment.objects.filter(Article__id=obj.pk).values('Article__id').annotate(a=Count('id'))
        # print(ret)
        ret=models.Comment.objects.filter(Article__id=obj.pk).values('Article__id').annotate(a=Count('id'))
        # print(ret.first())
        count=ret[0]['a']
        # print(count)
        return count
    def get_summary(self,obj):
        return obj.content[:50]
    def get_comments(self,obj):
        ret=models.Comment.objects.filter(Article__id=obj.pk).order_by('content_time')
        # comment_list=ret.values_list('content','content_time','zan')
        comments=ret.values('content','content_time','zan')
        return comments



class PageArticleView(APIView):
    def patch(self,request,*args,**kwargs):    # 查
        tid=request.GET.get('tid')
        # tid = kwargs.get('tid')
        print(tid)
        if tid=="0":
            queryset = models.Article.objects.all().order_by('create_at')
        else:
            queryset=models.Article.objects.filter(tag__tid=tid).order_by('create_at')

        page_object = PageNumberPagination()
        result=page_object.paginate_queryset(queryset,request,self)
        print(result,type(result))
        ser=PageArticleSerializer(instance=result,many=True)
        # return Response(ser.data)
        # return page_object.get_paginated_response(ser.data)
        print('page_object.page.paginator',page_object.page.paginator)
        return Response({'count':page_object.page.paginator.count,'result':ser.data})
    def get(self,request,*args,**kwargs):
        aid = request.GET.get('aid')
        queryset = models.Article.objects.filter(pk=aid)
        queryset.update(check=F('check')+1)
        page_object = PageNumberPagination()
        result = page_object.paginate_queryset(queryset, request, self)
        print(result, type(result))
        ser = PageArticleSerializer(instance=result, many=True)
        # return Response(ser.data)
        # return page_object.get_paginated_response(ser.data)
        return Response({'count': page_object.page.paginator.count, 'result': ser.data})


class PageCommentSerializer(serializers.ModelSerializer):
    # title = serializers.SerializerMethodField()
    # # create_at = serializers.SerializerMethodField()
    # check = serializers.SerializerMethodField()
    # content = serializers.SerializerMethodField()
    # comment_num = serializers.SerializerMethodField()
    # comment = serializers.SerializerMethodField()
    class Meta:
        model = models.Comment
        fields ='__all__'
    # def get_title(self,obj):
    #     return obj.Article.title
    # def get_create_at(self,obj):
    #     return obj.Article.create_at
    # def get_check(self,obj):
    #     return obj.Article.check
    # def get_content(self,obj):
    #     return obj.Article.content
    # def get_comment_num(self,obj):
    #     ret=models.Comment.objects.filter(Article__id=obj.Article__id).values('id').count('id')
    #     print(ret)
    #     return ret
    # def get_comment(self,obj):
# class CommentLimitOffsetPagination(LimitOffsetPagination):
#     max_limit=2
class PageCommentView(APIView):

    # def get(self, request, *args, **kwargs):
    #     aid=request.GET.get('aid')
    #     # pk= kwargs.get('pk')
    #     queryset = models.Comment.objects.filter(Article__id=aid).order_by('content_time')
    #     page_object = PageNumberPagination()
    #     result = page_object.paginate_queryset(queryset, request, self)
    #     print(result, type(result))
    #     ser = PageArticleSerializer(instance=result, many=True)
    #     return Response({'count': page_object.page.paginator.count, 'result': ser.data})
    def post(self,request, *args, **kwargs):
        ser = PageCommentSerializer(data=request.data)
        print(ser)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)



# 使用事务进行执行
# @transaction.atomic
# def viewfunc(request):
#     # This code executes inside a transaction.
#     do_stuff()

class ArticleView(APIView):
    versioning_class=URLPathVersioning
    def get(self,request,*args,**kwargs):
        print(request.version)
        print(request.versioning_scheme)
        return Response('OK')
    def post(self,request,*args,**kwargs):
        return Response('post')
