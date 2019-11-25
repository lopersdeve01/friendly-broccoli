import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.versioning import URLPathVersioning
from django.conf import settings
from django.db.models import Q
from api import models
from api.plugins import process_server_info
class ServerView(APIView):

    def get(self,request,*args,**kwargs):
        """ 返回今日未采集的服务器列表 """
        today = datetime.datetime.today()
        queryset = models.Server.objects.filter(status=1).filter(Q(last_date__isnull=True)|Q(last_date__lt=today)).values('hostname')
        host_list = [ item['hostname'] for item in queryset]

        print('获取今日未采集的资产',host_list)
        return Response(host_list)

    def post(self,request,*args,**kwargs):
        # 1. 获取到用户提交资产信息
        # 2. 保存到数据库（表关系）
        hostname = request.data.get('hostname')
        server_object = models.Server.objects.filter(hostname=hostname).first()
        if not server_object:
            return Response('主机不存在')

        print('汇报过来的数据',request.data['info'])
        # process_server_info(request.data['info'],server_object)

        """
        # 今日已经采集
        server_object.last_date = datetime.datetime.today()
        server_object.save()
        """

        return Response('发送成功')
