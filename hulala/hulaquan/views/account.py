import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.versioning import URLPathVersioning
from hulaquan import models


class LoginView(APIView):
    """
    登录接口
    """
    def post(self,request,*args,**kwargs):
        user_object = models.UserInfo.objects.filter(**request.data).first()
        if not user_object:
            return Response('登录失败')
        random_string = str(uuid.uuid4())
        user_object.token = random_string
        user_object.save()
        print('request.data',request.data)
        # request.user=request.data.get('username')
        print('user',request.user)
        print('random_string',random_string)
        return Response(random_string)

#{"username":"fff","password":"fff123"}