from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse,redirect
# # class LoginAuth(MiddlewareMixin):
#     # white_list=['/login/']
#     # def process_request(self,request):
#     #     print('the request is coming!')
#     #     path=request.path
#     #     if path in self.white_list:
#     #         status = request.session.get('is_login')
#     #         if not status:
#     #             return redirect('/login/')
#     #
#     # def process_response(self,request,response):
#     #     print('the request is far away!')
#     #     return response
class MD1(MiddlewareMixin):
    def process_request(self,request):
        print('the process_request in MD1')

    def process_response(self,request,response):
        print('the process_response in MD1')
        return response
    def process_review(self,request,view_func,view_args,view_kwargs):
        print('_'*80)
        print('the process_view in MD1')
        print(view_func,view_func.__name__)
    def process_exceptin(self,request,exception):
        print('exception')
        print('the exception in MD1')
        return HttpResponse(str(exception))
    def process_template_response(self,request,response):
        print('the process_template_response in MD1')
        return response





class MD2(MiddlewareMixin):
    def process_request(self,request):
        print('the process_request in MD2')

    def process_response(self,request,response):
        print('the process_response in MD2')
        return response
    def process_review(self,request,view_func,view_args,view_kwargs):
        print('_'*80)
        print('the process_view in MD2')
        print(view_func,view_func.__name__)
    def process_exceptin(self,request,exception):
        print('exception')
        print('the exception in MD2')
        return HttpResponse(str(exception))
    def process_template_response(self,request,response):
        print('the process_template_response in MD2')
        return response