
from rest_framework.views import APIView


class Article(APIView):
    authentication_classes = []
    def get(self,request,*args,**kwargs):
        pass
