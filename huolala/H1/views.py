from django.shortcuts import render
from . import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count,F
import time
# Create your views here.

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Article
        exclude=['author']
class ArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.ArticleDetail
        # fields='__all__'
        exclude=['article']
class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Article
        fields="__all__"                                                        # 查询文章

# 设计页面显示内容
# 由于文章表中没有详细内容，作者，部分字段格式为非显示字段，所以加上两个字段处理时间与分类
# 由于文章详细与文章量表采用的是一对一关系。较为简单，所以推荐使用source字段
class PageArticleSerializer(serializers.ModelSerializer):
    content=serializers.CharField(source='articledetail.content')
    author=serializers.CharField(source="author.username")
    category=serializers.CharField(source='get_category_display')
    date=serializers.SerializerMethodField()
    class Meta:
        model=models.Article
        fields='__all__'

    # category_choices = ((1, '资讯'), (2, '公司动态'), (3, '分享'), (4, '答疑'), (5, '其他'))
    # category = models.IntegerField(verbose_name='分类', choices=category_choices)
    # title = models.CharField(verbose_name='标题', max_length=32)
    # image = models.CharField(verbose_name='图片路径', max_length=128)
    # summary = models.CharField(verbose_name='简介', max_length=255)
    # comment_count = models.IntegerField(verbose_name='评论数', default=0)
    # read_count = models.IntegerField(verbose_name='浏览数', default=0)
    # author = models.ForeignKey('UserInfo', verbose_name='作者')
    # data = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)


    def get_date(self,obj):
        # print(obj.data)
        data1 = str(obj.data)[:-13]
        # print(data1)
        t1 = time.mktime(time.strptime(data1,'%Y-%m-%d %H:%M:%S'))
        # print('t1', t1)
        # t2=time.localtime(t3+3600*8)
        # print('t2',t2)
        strftime=time.strftime("%Y-%m-%d %H:%M", time.localtime(t1 + 3600 * 8))
        # print(strftime)
        # print(obj.data)
        return strftime

class ArticleView(APIView):
    def get(self,request,*args,**kwargs):
        pk=kwargs.get('pk')
        if not pk:
            condition={}
            category=request.query_params.get('category')
            if category:
                condition['category']=category
            queryset=models.Article.objects.filter(**condition).order_by('-data')
            paper=PageNumberPagination()
            result=paper.paginate_queryset(queryset,request,self)
            ser=PageArticleSerializer(instance=result,many=True)
            return Response(ser.data)
        else:
            article_object=models.Article.objects.filter(pk=pk).first()
            ser= PageArticleSerializer(instance=article_object,many=False)
        return Response(ser.data)
    def post(self,request,*args,**kwargs):                                                   # 查询文章，添加文章
        ser_artcile=ArticleSerializer(data=request.data)
        ser_detail=ArticleDetailSerializer(data=request.data)
        if ser_artcile.is_valid() and ser_detail.is_valid():
            ser_artcile.save(author=1)
            ser_detail.save(article=ser_artcile)
            print(ser_artcile)
            print(ser_detail)
            return Response('添加成功')
        return Response('添加失败')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Comment
        fields="__all__"

class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Comment
        exclude=['user']

class CommentView(APIView):
    def get(self,request,*args,**kwargs):                                                # 查询评论，添加评论
        # pk=kwargs.get('pk')
        # article_id=kwargs.get('article_id')
        # article_id=request.query_params.get('article_id')   # 请求体中获取值
        article_id=request.GET.get('article_id')     # 请求头中获取值
        queryset=models.Comment.objects.filter(article_id=article_id)
        ser=CommentSerializer(instance=queryset,many=True)
        print(ser)
        return Response(ser.data)
    def post(self,request,*args,**kwargs):
        user_id = request.query_params.get('user_id')
        ser=PostCommentSerializer(data=request.data)
        if ser.is_valid():
            ser.save(user_id=user_id)
            return Response(ser.data)
        return Response('添加失败')






