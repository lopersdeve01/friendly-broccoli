from django.shortcuts import render
from rest_framework.response import Response
from V1 import models
from rest_framework.views import APIView
from rest_framework import serializers

from rest_framework.generics import GenericAPIView,ListAPIView,CreateAPIView,DestroyAPIView,RetrieveAPIView

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin,RetrieveModelMixin,CreateModelMixin,UpdateModelMixin,DestroyModelMixin
from rest_framework.viewsets import ModelViewSet

from rest_framework.throttling import AnonRateThrottle,BaseThrottle



class Show_article(serializers.ModelSerializer):
    img=serializers.SerializerMethodField()
    category=serializers.CharField(source='get_category_display')
    status=serializers.SerializerMethodField()
    author=serializers.SerializerMethodField()
    content=serializers.SerializerMethodField()
    create_at=serializers.SerializerMethodField()
    # comment_count=serializers.SerializerMethodField()
    class Meta:
        model=models.Article
        fields="__all__"
    def get_img(self,obj):
        # return obj.img.values('name','url')
        ret=models.Img.objects.filter(articles=obj.pk).values('name','url')
        # 尽量不要反向查询
        return ret
    def get_status(self,obj):
        return obj.get_category_display()
    def get_author(self,obj):
        return obj.author.name
    def get_content(self,obj):
        return obj.articledetails.content
    # def get_comment_count(self,obj):
    #     ret=models.Comment.objects.filter(articles_id=obj.pk).Count('id')
    #     return ret
    def get_create_at(self,obj):
        return obj.create_at.strftime('%Y-%m-%d %H:%M:%S') if obj.create_at else ''
class Save_article(serializers.ModelSerializer):
    class Meta:
        model=models.Article
        exclude=['author']

class Articledetails(serializers.ModelSerializer):
    class Meta:
        model=models.ArticleDetails
        exclude=['articles']

class Show_comment(serializers.ModelSerializer):
    class Meta:
        model=models.Comment
        exclude=['articles']
# Create your views here.


# class Article(ListAPIView):
#     authentication_class=[]
#     queryset=models.Article.objects.all()
#     serliazer_class=Show_article


class ArticleView(GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin,
                  DestroyModelMixin):
# class Article(ModelViewSet):
    authentication_classes = []
    throttle_classes = [AnonRateThrottle, ]

    queryset = models.Article.objects.all()
    serializer_class = None

    def get_serializer_class(self):
        pk = self.kwargs.get('pk')
        if pk:
            return Articledetails
        return Show_article
    def create(self,request,*args,**kargs):
        pass
        return Response("OK")