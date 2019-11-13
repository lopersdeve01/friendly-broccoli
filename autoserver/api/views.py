from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.
class ServerView(APIView):
    def post(self,request,*args,**kwargs):
        print(request.data)
        return Response('发送成功')
    def get(self,request,*args,**kwargs):
        """ 返回今日未采集的服务器列表 """
        host_list = ["192.168.153.128",]
        return Response(host_list)