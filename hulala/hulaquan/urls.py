from django.conf.urls import url

from hulaquan.views import views,account,article,comment

urlpatterns = [
    url(r'^home/article/$', views.PageArticleView.as_view()),
    # # url(r'^category/article/$', views.PageArticleView.as_view()),
    # url(r'^page/article/$', views.PageArticleView.as_view()),
    # url(r'^page/article/(?P<pk>\d+)/$', views.PageCommentView.as_view()),
    url(r'^page/article/$', views.PageCommentView.as_view()),
    url(r'^(?P<version>\w+)/users/$', views.ArticleView.as_view(), name='users_list'),
    url(r'^page/article/$', views.PageCommentView.as_view()),

    url(r'^login/$', account.LoginView.as_view()),
    # # url(r'^category/article/$', views.PageArticleView.as_view()),
    # url(r'^page/article/$', views.PageArticleView.as_view()),
    # url(r'^page/article/(?P<pk>\d+)/$', views.PageCommentView.as_view()),
    url(r'^article/$', article.NewArticleView.as_view()),
    # url(r'^page/article/$', views.PageCommentView.as_view()),
    url(r'^comment/$', comment.CommentView.as_view()),
]
