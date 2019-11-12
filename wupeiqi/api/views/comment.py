
from rest_framework.views import APIView
from rest_framework.response import Response


class CommentView(APIView):
    def get(self,request,*args,**kwargs):
        return Response('所有评论')
    def post(self,request,*args,**kwargs):
        return Response('添加评论')
    def get_authenticators(self):
        if self.request.method=="GET":
            return []
        elif self.request.method=='POST':
            return super().get_authenticators()