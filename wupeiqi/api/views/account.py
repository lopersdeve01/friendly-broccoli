from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from api import models

from rest_framework.throttling import AnonRateThrottle,BaseThrottle


class LoginView(APIView):
    def post(self,request,*args,**kwargs):
        print(request.data)
        user=models.UserInfo.objects.filter(username=request.data.get('username'),password=request.data.get('password')).first()
        if not user:
            return Response({'code':10000,'error':'用户名或者密码错误'})
        jwt_payload_handler=api_settings.JWT_PAYLOAD_HANDLER
        payload=jwt_payload_handler(user)

        jwt_encode_handler=api_settings.JWT_ENCODE_HANDLER
        token=jwt_encode_handler(payload)
        return Response({'code':10000,'data':token})
