from django.conf.urls import url
from django.contrib import admin
from V1 import views,views1


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^info/', views.InfoView.as_view()),
    # url(r'^info/$', views.DrfInfoView.as_view()),
    # url(r'^drf/category/', views1.DrfCategoryView.as_view()),
    url(r'^drf/article/$', views1.ArticleView.as_view()),
    url(r'^drf/article/(?P<pk>\d+)/$', views1.ArticleView.as_view()),
    # url(r'^drf/article1/$', views.NewArticleSerializer.as_view()),
    # url(r'^drf/article1/(?P<pk>\d+)/$', views.NewArticleSerializer.as_view()),
    # url(r'^page/article/$', views.PageArticleView.as_view()),
    url(r'^page/article/(?P<pk>\d+)/$', views1.CommentView.as_view()),
]
urlpatterns += [
    url(r'^login/$', views.LoginView.as_view()),
    url(r'^article/$', views.ArticleView.as_view()),
    url(r'^article_add/$',views.Add_Article.as_view()),
    url(r'^single_article/(?P<pk>\d+)/$',views.SingleAritcle.as_view()),
    url(r'^(?P<version>\w+)/article/$', views.ArticleView.as_view()),
    url(r'^page/article/(?P<pk>\d+)/$', views.CommentView.as_view()),

# {"category":"2","content":"bbbb","title":"ffffff","comment_count":4}


]
