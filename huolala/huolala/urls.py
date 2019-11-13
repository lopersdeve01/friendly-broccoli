"""huolala URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from H1 import views

urlpatterns = [
    url(r'^admin/',admin.site.urls),
    url(r'^home/article/$',views.ArticleView.as_view()),
    url(r'^home/article/(?P<pk>\d+)/$',views.ArticleView.as_view()),
    url(r'^page/article/$', views.CommentView.as_view()),
    url(r'^page/article/(?P<pk>\d+)/$',views.CommentView.as_view()),
]


# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
#
# ]
urlpatterns += [
    url(r'^v1/', include('V1.urls',namespace="V1")),
]
urlpatterns += [
    url(r'^v2/', include('V2.urls',namespace="V2")),
]
# urlpatterns += [
#     url(r'^page/article/$', views.CommentView.as_view()),
# ]
