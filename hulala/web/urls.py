from django.conf.urls import url

from web.views import views

urlpatterns = [

    url(r'^login/$', views.LoginView.as_view()),
    # # url(r'^category/article/$', views.PageArticleView.as_view()),
    # url(r'^page/article/$', views.PageArticleView.as_view()),
    # url(r'^page/article/(?P<pk>\d+)/$', views.PageCommentView.as_view()),
    url(r'^order/$', views.OrderView.as_view()),
    url(r'^user/$', views.UserView.as_view()),

    # url(r'^page/article/$', views.PageCommentView.as_view()),
]
