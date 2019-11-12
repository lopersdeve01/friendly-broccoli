from django.shortcuts import render
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse
from server import models

from rest_framework.views import APIView
from rest_framework.response import Response
from django.forms.models import model_to_dict
from rest_framework import serializers
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import  ListAPIView,GenericAPIView

# Create your views here.


class PageArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Article
        fields='__all__'
class PageArticleView(APIView):
    def get(self,request,*args,**kwargs):
        cid = kwargs.get('categorys_id')
        # cid=request.GET.get('category')
        queryset=models.Article.objects.filter(category=cid)

        page_object = PageNumberPagination()
        result=page_object.paginate_queryset(queryset,request,self)
        print(result,type(result))
        ser=PageArticleSerializer(instance=result,many=True)
        # return Response(ser.data)
        # return page_object.get_paginated_response(ser.data)
        return Response({'count':page_object.page.paginator.count,'result':ser.data})


class PageCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = '__all__'

class PageCommentView(APIView):
    def get(self, request, *args, **kwargs):
        pk= kwargs.get('pk')
        queryset = models.Article.objects.all()
        page_object = PageNumberPagination()
        result = page_object.paginate_queryset(queryset, request, self)
        print(result, type(result))
        ser = PageArticleSerializer(instance=result, many=True)
        # return Response(ser.data)
        # return page_object.get_paginated_response(ser.data)
        return Response({'count': page_object.page.paginator.count, 'result': ser.data})
    # def post(self,request, *args, **kwargs):



