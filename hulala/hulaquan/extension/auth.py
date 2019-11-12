from hulaquan import models
from rest_framework.authentication import BaseAuthentication

class LuffyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        print('LuffyAuthentication')
        """
        Authenticate the request and return a two-tuple of (user, token).
        """
        token = request.query_params.get('token')
        print(token)
        if not token:
            return (None,None)
        print('token',token)

        user_object = models.UserInfo.objects.filter(token=token).first()
        if user_object:
            return (user_object,token)
        return (None,None)
