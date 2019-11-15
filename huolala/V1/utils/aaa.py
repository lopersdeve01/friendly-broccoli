import jwt
from V1 import models
from rest_framework.permissions import BasePermission
from rest_framework.authentication import BaseAuthentication
from rest_framework.throttling import AnonRateThrottle,BaseThrottle
from rest_framework import exceptions
from rest_framework_jwt.settings import api_settings



class Authentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.query_params.get('token')
        print('token',token)
        user_object = models.User.objects.filter(token=token).first()
        # print("user_object",user_object.username)
        if not token:
            raise exceptions.AuthenticationFailed({"code":"10002","error":"登陆之后才能操作"})
        # user_object = models.User.objects.filter(token=token).first()
        # print('user_object',user_object)
        # if user_object:
        #     return (user_object,token)
        # return (None,None)
        print(111)
        jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
        try:
            print(222)
            payload = jwt_decode_handler(token)
            print('是不是没下来')
            print('payload',payload)
            jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER
            username = jwt_get_username_from_payload(payload)
            user_object = models.User.objects.filter(username=username).first()
            print('username', username)
        except jwt.ExpiredSignature:
            print(11)
            raise exceptions.AuthenticationFailed({'code': "10003", "error": "token已过期"})
        except jwt.DecodeError:
            print(22)
            raise exceptions.AuthenticationFailed({'code': "10004", "error": "token格式错误"})
        except jwt.InvalidTokenError:
            print(33)
            raise exceptions.AuthenticationFailed({'code': "10005", "error": "认证失败"})
        print(444)


        return (user_object, token)

# class AnnoyAuthentication(BaseAuthentication):
#     def authenticate(self, request):
#         token=request.query_params.get('token')
#         print('token',token)




class Permission(BasePermission):
    message = {"status":False,"error":"登录成功之后才能评论"}
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        if request.user:
            return True
        return False


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
