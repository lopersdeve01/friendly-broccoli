from rest_framework.authentication import BaseAuthentication
from web import models
class TokenAuthenticaton(BaseAuthentication):

    def authenticate(self,request):
        print('TokenAuthenticaton')
        token=request.query_params.get('token')
        print('token',token)
        user_object=models.UserInfo.objects.filter(token=token).first()
        if user_object:
            return (user_object,token)
        return (None,None)