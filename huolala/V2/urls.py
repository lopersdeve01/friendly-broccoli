from django.conf.urls import url
from django.contrib import admin
from V2 import views


urlpatterns = [
    url(r'^article/$', views.ArticleView.as_view({'get':'list','post':'create'})),
    url(r'^article/(?P<pk>\d+)/$', views.ArticleView.as_view({'get':'retrieve'})),
]

