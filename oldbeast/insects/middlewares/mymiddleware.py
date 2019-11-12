from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse,redirect
class LoginAuth(MiddlewareMixin):
    white_list=[reverse('/login/'),reverse('register')]
    def process_request(self,request):
        print('the request is coming!')
        path=request.path
        if path in self.white_list:
            user = request.session.get('username')
            if not user:
                return redirect('/login/')

    def process_response(self,request,response):
        print('the request is far away!')
        return response
