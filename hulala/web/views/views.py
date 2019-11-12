from django.shortcuts import render

from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from web import models



import uuid
from rest_framework.versioning import URLPathVersioning
from .auth import TokenAuthenticaton
from rest_framework.permissions import BasePermission
from rest_framework import exceptions


# Create your views here.

class LoginView(APIView):
    authentication_classes = [TokenAuthenticaton]
    def post(self,request,*args,**kwargs):
        user_object=models.UserInfo.objects.filter(**request.data).first()
        if not user_object:
            return Response("登陆失败")
        random_string=str(uuid.uuid4())
        user_object.token=random_string
        user_object.save()
        return Response(random_string)


class MyPermission(BasePermission):
    print(111,'MyPermission')
    message={'code':10001,'error':'你没有权限'}
    def has_permission(self,request,view):
        if request.user:
            return True
        return False
    def has_object_permission(self,request,vew,obj):
        return False


class OrderView(APIView):
    authentication_classes = [TokenAuthenticaton]
    permission_classes = [MyPermission]
    def get(self,request,*args,**kwargs):
        return Response('order')


class UserView(APIView):
    authentication_classes = [TokenAuthenticaton]
    permission_classes = [MyPermission]
    def get(self,request,*args,**kwargs):
        return Response('user')




