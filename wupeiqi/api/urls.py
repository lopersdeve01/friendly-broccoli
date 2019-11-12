
from django.conf.urls import url,include
from django.contrib import admin
from .views import account,order,comment
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.utils import jwt_encode_handler

urlpatterns = [
    url(r'^login/$',account.LoginView.as_view()),
    url(r'^order/$', order.OrderView.as_view()),
    url(r'^comment/$', comment.CommentView.as_view()),
]