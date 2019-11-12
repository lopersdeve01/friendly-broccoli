
from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.shortcuts import redirect,HttpResponse,render

class Auth(MiddlewareMixin):
    white_list = [reverse('sales:login'),reverse('sales:register'),]
    def process_request(self,request):
        if request.path not in self.white_list:
            username = request.session.get('username')
            if not username:
                return redirect('sales:login')
        print('the reuqest is coming!')
    def process_response(self,request,response):
        print('the request is far away!')
        return response























