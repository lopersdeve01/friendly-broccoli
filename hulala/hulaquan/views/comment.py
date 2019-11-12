from rest_framework.views import APIView
from rest_framework.response import Response
from hulaquan.extension.permission import LuffyPermission
from hulaquan.extension.auth import LuffyAuthentication
class CommentView(APIView):
    authentication_classes = [LuffyAuthentication,]
    permission_classes = [LuffyPermission,]


    def get(self, request, *args, **kwargs):
        return Response('获取所有评论')

    def post(self,request,*args,**kwargs):
        print('request.user', request.user)
        if request.user:
             # 可以评论
            return Response('thanks for your perfect comments!')
        return Response('Please login first！')

# {"content":"Nice","content_time":"2019-11-01 15:51:33.000000","Article":"1"}