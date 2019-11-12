import jwt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework import exceptions
from api import models

from rest_framework.throttling import AnonRateThrottle,BaseThrottle

from rest_framework.authentication import BaseAuthentication
class HulaQueryParamAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token=request.query_params.get('token')
        print('token',token)
        if not token:
            raise exceptions.AuthenticationFailed({"code":"10002","error":"登陆之后才能操作"})

        jwt_decode_handler=api_settings.JWT_DECODE_HANDLER
        try:
            payload=jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            raise exceptions.AuthenticationFailed({'code': "10003", "error": "token已过期"})
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed({'code': "10004", "error": "token格式错误"})
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed({'code': "10005", "error": "认证失败"})

        jwt_get_username_from_payload=api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER
        username=jwt_get_username_from_payload(payload)
        user_object=models.UserInfo.objects.filter(username=username).first()
        return (user_object,token)


# {"username":"aaa","password":"aaa123","token":
# "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFhYSIsImV4cCI6MTU3MzQ2NDQ1Nn0.NUbkHD3SdjPCpteZyoOXKqdoxpINRpBtJRweLKjY2s0"}

        #
        # return Response({'code':10000,'data':token})
        #
        # jwt_payload_handler=api_settings.JWT_PAYLOAD_HANDLER
        # payload=jwt_payload_handler(user)
class RateThrottle(AnonRateThrottle):
    def get_cache_key(self, request, view):
        # if request.user:
        #     if request.user.is_authenticated:
        #         return None  # Only throttle unauthenticated requests.
        print('request.user',request.user)
        if request.user:
            print(request.user.username)
            # if request.user.is_authenticated: # django-admin 中的验证方式，UserInfo中不适合验证
            #     return self.cache_format % {
            # 'scope': self.scope,
            # 'ident': request.user}
            # else:
            #     return Response('认证失败')

            return self.cache_format % {
        'scope': self.scope,
        'ident': request.user}

        else:
            return self.cache_format % {
                'scope': self.scope,
                'ident': self.get_ident(request)
            }




class OrderView(APIView):
    authentication_classes = [HulaQueryParamAuthentication,]
    throttle_classes = [RateThrottle,]
    def get(self,request,*args,**kwargs):
        print(request.user)
        # print(request.user.username)
        print(request.auth)
        return Response('订单列表')


def post(self,request,*args,**kwargs):

    return Response('添加订单')