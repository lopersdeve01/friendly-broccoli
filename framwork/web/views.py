from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse
from web import models

from rest_framework.views import APIView
from rest_framework.response import Response
from django.forms.models import model_to_dict
from rest_framework import serializers
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView,GenericAPIView


# Create your views here.


class InfoView(View):
    def info(self):
        pass


class DrfInfoView(APIView):
    def info(self):
        pass


class DrfCategoryView(APIView):

    def get(self,request,*args,**kwargs):
        # title=request.GET.get('title')
        # ret=models.Article.objects.all().values_list('categorys__id','categorys__name').distinct()
        # category=ret  # 使用双下环线进行筛选，实现跨表字段查询，可以针对queryset类型，无论单个或者多个数据
        # 使用values_list生成格式为列表类型，若要传输，需要加上safe=falseh，或者拼接为字典格式
        # ret=models.Article.objects.all().first()
        # category=ret.categorys.values('id','name').distinct() #此类方法适用于manytomanyfield

        # data={'category':category}
        # ret=models.Category.objects.all().values('id','name')
        # data=list(ret)
        # return Response(data)

        pk=kwargs.get('pk')  # 不同请求方法下，获取前台传输数据，
        if not pk:
            queryset=models.Category.objects.all().values_list('id','name')
            data_list=list(queryset)
            return Response(data_list)
        else:
            category_object = models.Category.objects.filter(id=pk).first()
            data=model_to_dict(category_object)
            return Response(data)
    def post(self,request,*args,**kwargs):
        # data = request.POST.dict()
        name=request.POST.get('name')
        # name='IT'
        models.Category.objects.create(name=name )
        # models.Category.objects.create(
        #     **request.data )
        return Response('OK')
    def delete(self,request,*args,**kwargs):
        # 注意带参数
        pass
        return Response('OK')
    def put(self,request,*args,**kwargs):
        # 注意带参数
        pass
        return Response('OK')


# class DrfArticleView(APIView):
#     def post(self,request,*args,**kwargs):   # 增
#         ret=models.Article.objects.create(**request.data)
#         data={'ret':ret}
#         return JsonResponse(data)
#
#     def get(self,request,*args,**kwargs):    # 查
#         pk=kwargs.get('pk')
#         if pk:
#             print(pk)
#             ret=models.Article.objects.filter(pk=pk).values('pk','title','summary','content','categorys__pk','categorys__name')
#         else:
#             ret=models.Article.objects.all().values_list('pk','title','summary','content','categorys__pk','categorys__name').distinct()
#         data={'ret':ret}
#         return Response(data)
#{"title":"标题","summary":"简介","content":"容","categorys_id":"3"}
#     def delete(self,request,*args,**kwargs): # 删
#         pk = kwargs.get('pk')
#         models.Article.objects.filter(pk=pk).delete()
#         return Response('DONE')
#
#     def put(self,request,*args,**kwargs):    # 改
#         pk = kwargs.get('pk')
#         ret=models.Article.objects.filter(pk=pk).update(**request.data)
#         data={'ret':ret}
#         return JsonResponse(data)
# class NewArticleSerializer(serializers.ModelSerializer):
#     class Meta:
#         # x1=serializers.CharField(source='category.name')
#         status_txt=serializers.CharField(source='get.status.display',required=False)
#         model=models.Article
#         fileds=['pk','title','content','summary','category','status_txt','x2']
#         # fields='__all__'
#         # depth=1
#         def x1(self,obj):
#             return obj.category.name
#         def x2(self,obj):
#             return obj.get.status.display()
#
#
# class DrfArticleView(APIView):
#     def post(self,request,*args,**kwargs):
#         ser=NewArticleSerializer(data=request.data)
#         if ser.is_valid():
#             ser.save()
#             return Response(ser.data)
#         return Response(ser.errors)
#     def get(self,request,*args,**kwargs):
#         pk=kwargs.get('pk')
#         if pk:
#             print(pk)
#             queryset = models.Article.objects.filter(pk=pk).first()
#             ser=NewArticleSerializer(instance=queryset,many=False)
#             return Response(ser.data)
#         else:
#             queryset = models.Article.objects.all()
#             ser=NewArticleSerializer(instance=queryset,many=True)
#             return Response(ser.data)
#
#     def delete(self,request,*args,**kwargs):
#         pk=kwargs.get('pk')
#         models.Article.objects.filter(pk=pk).delete()
#         return Response('DONE')
#     def put(self,request,*args,**kwargs): # 全部更新
#         pk=kwargs.get('pk')
#         queryset = models.Article.objects.filter(pk=pk).first()
#         ser=NewArticleSerializer(data=request.data,instance=queryset)
#         if ser.is_valid():
#             ser.save()
#             return Response(ser.data)
#         return Response(ser.errors)
#
#
#     def patch(self,request,*args,**kwargs): # 局部更新
#         pk=kwargs.get('pk')
#         queryset = models.Article.objects.filter(pk=pk).first()
#         ser=NewArticleSerializer(data=request.data,instance=queryset,partial=True)
#         if ser.is_valid():
#             ser.save()
#             return Response(ser.data)
#         return Response(ser.errors)





class NewArticleSerializer(serializers.ModelSerializer):
    x1 = serializers.SerializerMethodField()
    x2 = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    status_txt=serializers.CharField(source='get_status_display',required=False)
    class Meta:
        # x1=serializers.CharField(source='categorys.name')
        # x1=serializers.CharField(source='title')
        model=models.Article
        fields =['pk','title','content','summary','categorys','x2','x1','tags','status_txt']
        # fields='__all__'
        # depth=1
    def get_x1(self,obj):
        return obj.categorys.name
    def get_x2(self,obj):
        return obj.get_status_display()
    def get_tags(self,obj):
        # return obj.tags.values_list('pk','title')
        return obj.tags.values('pk','title')
        # objs=obj.tags.all()
        # print(type(obj.tags))  # <class 'django.db.models.fields.related_descriptors.
        # # create_forward_many_to_many_manager.<locals>.ManyRelatedManager'>
        # print(type(objs))     # <class 'django.db.models.query.QuerySet'> queryset对象
        # return [{'id':i.id,'title':i.title} for i in objs]
        # return obj.title
        # return [row for row in obj.tags.all().values('pk','title')]



class DrfArticleView(APIView):
    def post(self,request,*args,**kwargs):
        ser=NewArticleSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)
    def get(self,request,*args,**kwargs):
        pk=kwargs.get('pk')
        if pk:
            print(pk)
            queryset = models.Article.objects.filter(pk=pk).first()
            ser=NewArticleSerializer(instance=queryset,many=False)
            return Response(ser.data)
        else:
            queryset = models.Article.objects.all()
            ser=NewArticleSerializer(instance=queryset,many=True)
            return Response(ser.data)

    def delete(self,request,*args,**kwargs):
        pk=kwargs.get('pk')
        models.Article.objects.filter(pk=pk).delete()
        return Response('DONE')
    def put(self,request,*args,**kwargs): # 全部更新
        pk=kwargs.get('pk')
        queryset = models.Article.objects.filter(pk=pk).first()
        ser=NewArticleSerializer(data=request.data,instance=queryset)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)


    def patch(self,request,*args,**kwargs): # 局部更新
        pk=kwargs.get('pk')
        queryset = models.Article.objects.filter(pk=pk).first()
        ser=NewArticleSerializer(data=request.data,instance=queryset,partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)



class PageArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Article
        fields='__all__'
class PageArticleView(APIView):
    def get(self,request,*args,**kwargs):
        queryset=models.Article.objects.all()
        page_object = PageNumberPagination()
        result=page_object.paginate_queryset(queryset,request,self)
        print(result,type(result))
        ser=PageArticleSerializer(instance=result,many=True)
        # return Response(ser.data)
        # return page_object.get_paginated_response(ser.data)
        return Response({'count':page_object.page.paginator.count,'result':ser.data})



