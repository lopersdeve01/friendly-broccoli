from django.shortcuts import render
from rest_framework.views import APIView
from V1 import models
from rest_framework import serializers

from rest_framework.response import Response
from rest_framework.filters import BaseFilterBackend
from rest_framework_jwt.settings import api_settings

from django.db.models import F,Count

import uuid



# Create your views here.
# 类处理方法
# 实现文章的增删改查
# 实现评论的增删该查
# 实现分页，版本，认证，权限，截留等处理

# 首先定义功能类（分页，版本，认证，权限，截留）

# 分页的实例化
# 需要引入如类
from rest_framework.pagination import PageNumberPagination
# 使用时，先将类实例化
# page_object = PageNumberPagination()
# ，再将queryset放进result进行校正
# result=page_object.paginate_queryset(queryset,request,self)
# 将数据放进ser类中进行格式化
#  ser=PageArticleSerializer(instance=result,many=True)
# 返回数据{'page':page_object.page.paginator.count,'result':ser.data}
# return Response(ser.data)                                                      # 仅返回数据
# return page_object.get_paginated_response(ser.data)                            # 数据+分页信息
# return Response({'count':page_object.page.paginator.count,'result':ser.data})  # 自定制分页部分数据与全部返回数据

# 同样对于每页不固定显示
from rest_framework.pagination import LimitOffsetPagination
# 实例化操作与PageNumberPagination类似
# page_object = HulaLimitOffsetPagination()
# result = page_object.paginate_queryset(queryset, request, self)
# ser = PageArticleSerializer(instance=result, many=True)
# return Response(ser.data)

# 引入批量操作
from rest_framework.generics import GenericAPIView,ListAPIView,CreateAPIView,DestroyAPIView,RetrieveAPIView
# 进行条件设定
# 分页设定——————根据情况设置
# pagination_class = PageNumberPagination
# 假如没有特别的分页需求，系统默认选用配置settings文件中的，如果有特殊要求，可以在类中进行提交，实现自定制

# 筛选处理————必设
# django内置筛选函数，如果需要筛选，将筛选参数进行设置，并提交
# def filter_queryset(self,queryset):
#     for backend in list(self.filter_backends):
#         queryset=backend().filter_queryset(self.request,queryset,self)
#         return queryset
# 设置筛选条件
# filter_backends=[NewfilterBackend,]

# 序列化设置————必设
# 需要制定序列化类时，将序列化参数自定制进行提交，
# serializer_class = NewSerializers


# 版本设置
# 引入类/前者为针对请求体中的？后者针对路径中存在参数进行处理
from rest_framework.versioning import QueryParameterVersioning,URLPathVersioning
# 配置路由
# url(r'^(?P<version>\w+)/users/$', views.ArticleView.as_view(),name='users_list'),
# 设置MyVersion类，并查看其中的函数determine_version
# class MyVersion(object):
#     def determine_version(self,request,*kwargs,**kwaargs):
#         return kwargs.get('version')
# 视图函数关于版本的类设置，需要进行单独定制版本类属性——————必设
# class ArticleView(APIView):
#     versioning_class=URLPathVersioning
#     def get(self,request,*args,**kwargs):
#     def post(self,request,*args,**kwargs):
# settings中配置全局文件
# "DEFAULT_VERSION": "v1",
# "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
# "ALLOWED_VERSIONS": ['v1', 'v2'],
# 'VERSION_PARAM': 'version',

# 认证设置——基于认证随机字符串的token的验证
# 建表之初应该设设置token字段，并默认为空
# 引入类
from rest_framework.authentication import BaseAuthentication
# 设置TokenAuthentication，并重置函数authenticate，进行自定制函数功能
# class TokenAuthentication(BaseAuthentication):
#     def authenticate(self, request):
#         token = request.query_params.get('token')   # 将token放置在请求路径中，进行验证
#         user_object = models.UserInfo.objects.filter(token=token).first()  #  假如用户信息表中有此token，默认通过认证，即完成登陆
#         if user_object:
#             return (user_object,token)
#         return (None,None)
# 视图函数关于认证的类设置，需要进行单独定制版本类属性——————必设
# class OrderView(APIView):
    # authentication_classes = [TokenAuthentication, ]
    # permission_classes = [MyPermission,]
    # def get(self,request,*args,**kwargs):
    #     return Response('order')
# settings中配置全局文件，作为全局变量设置
#"DEFAULT_AUTHENTICATION_CLASSES": ["hulaquan.extension.auth.LuffyAuthentication", ],

# 权限设置
# 引入类
from rest_framework.permissions import BasePermission
#引入排除权限
from rest_framework import exceptions
# 设置MyPermission，并重置函数has_permission（针对多个变量）与has_object_permission（针对单个变量），并设置错误信息，
# 进行自定制函数功能
# class MyPermission(BasePermission):
#     message = {'code': 10001, 'error': '你没权限'}
#     def has_permission(self, request, view):
#         if request.user:   # 假如存在用户，request.user为drf默认设置,但是此类权限验证只是较为基础的验证，并没有根据用户设置权限。
#         if request.user.login_type != 3:    #对于出现用户权限认证，进行进一步判断
#             return True    # 简单对用户名进行判定，检验是否具备具备此权限
                # (3).继承于BasePermission的自定义permission类必须重写一个函数，那就是has_permission(),他其实返回的就是一个布尔值，
                # 比如我有一些数据，必须是login_tyoe为3的用户SVip才能访问，则equest.user.login_type != 3 返回False.
                # 在内部会直接做一个判断，如果是False直接就是抛出一个异常结束。如果返回的是True,则通过权限检验，进入self.dispatch()进行反射去找method.
                # 原文链接：https://blog.csdn.net/weixin_40310390/article/details/98350642
#         # raise exceptions.PermissionDenied({'code': 10001, 'error': '你没权限'})  # 可以提供报错，阻断return后的判断
#         return False
#     def has_object_permission(self, request, view, obj):
#         return False
# 视图函数关于权限的类设置，需要进行单独定制版本类属性——————必设
# class OrderView(APIView):
    # permission_classes = [MyPermission,]
    # authentication_classes = [TokenAuthentication, ]
    # def get(self,request,*args,**kwargs):
    #     return Response('order')
# settings中配置全局文件，作为全局变量设置
# "DEFAULT_PERMISSION_CLASSES": ["hulaquan.extension.permission.LuffyPermission", ],

# 分留设置

# 操作类
from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveAPIView,DestroyAPIView,UpdateAPIView



    # def has_object_permission(self, request, view, obj):
    #     """
    #     Return `True` if permission is granted, `False` otherwise.
    #     """
    #     return False

class LoginView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self,request,*args,**kwargs):
        print(request.data)
        user = models.User.objects.filter(**request.data).first()
        if not user:
            return Response('登录失败')
        random_string = str(uuid.uuid4())
        user.token = random_string
        user.save()

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        payload = jwt_payload_handler(user)
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        token = jwt_encode_handler(payload)
        # return Response(random_string,{'code':10000,'data':token})
        return Response({'code':10000,'data':token})
# class LoginView(APIView):
#     def post(self,request,*args,**kwargs):
#         print(request.data)
#         user=models.UserInfo.objects.filter(username=request.data.get('username'),password=request.data.get('password')).first()
#         if not user:
#             return Response({'code':10000,'error':'用户名或者密码错误'})
#         jwt_payload_handler=api_settings.JWT_PAYLOAD_HANDLER
#         payload=jwt_payload_handler(user)
#
#         jwt_encode_handler=api_settings.JWT_ENCODE_HANDLER
#         token=jwt_encode_handler(payload)
#         return Response({'code':10000,'data':token})




# class MyPermission(BasePermission):
#     message = {'code': 10001, 'error': '你没权限'}
#     def has_permission(self, request, view):
#         if request.user:
#             return True
#
#         # raise exceptions.PermissionDenied({'code': 10001, 'error': '你没权限'})
#         return False

    # def has_object_permission(self, request, view, obj):
    #     """
    #     Return `True` if permission is granted, `False` otherwise.
    #     """
    #     return False

# class OrderView(APIView):
#     # authentication_classes = [TokenAuthentication, ]
#     permission_classes = [Permission,]
#     def get(self,request,*args,**kwargs):
#         return Response('order')
#
#
# class UserView(APIView):
#     # authentication_classes = [TokenAuthentication,]
#     permission_classes = [Permission, ]
#     def get(self,request,*args,**kwargs):
#         return Response('user')





class Show_article(serializers.ModelSerializer):
    img=serializers.SerializerMethodField()
    category=serializers.CharField(source='get_category_display')  # 自定制字段与表格字段相同，会对原表格字段进行显示覆盖
    status=serializers.SerializerMethodField()
    author=serializers.SerializerMethodField()
    content=serializers.SerializerMethodField()
    # comment_count=serializers.SerializerMethodField()
    # 自定制时间类型
    # create_at=serializers.SerializerMethodField()
    class Meta:
        model=models.Article
        fields="__all__"
    def get_img(self,obj):
        # return obj.img.values('name','url')
        ret=models.Img.objects.filter(articles=obj.pk).values('name','url')
        # 尽量不要反向查询
        return ret
    def get_status(self,obj):
        return obj.get_category_display()
    def get_author(self,obj):
        return obj.author.name
    def get_content(self,obj):
        return obj.articledetails.content
    # def get_comment_count(self,obj):
    #     ret=models.Comment.objects.filter(articles_id=obj.pk).Count('id')
    #     return ret
class Save_article(serializers.ModelSerializer):
    class Meta:
        model=models.Article
        fields="__all__"
        # exclude=['author']

class Articledetails(serializers.ModelSerializer):
    class Meta:
        model=models.ArticleDetails
        exclude=['articles']
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = "__all__"
class Save_comment(serializers.ModelSerializer):
    class Meta:
        model=models.Comment
        exclude=['articles','users']


class FilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # val=request.GET.get('cagetory')
        val = request.query_params.get('cagetory')
        print('val',val)
        if val:
            ret=queryset.filter(category=val)
        else:
            ret=queryset
        return ret
# class SingleFilterBackend(BaseFilterBackend):
#     def filter_queryset(self,request,queryset,view):
#         pk=request.query_params.get('pk')
#         print('pk',pk)
#         return queryset.filter(pk=pk)
class CommentFilterBackend(BaseFilterBackend):
    def filter_queryset(self,request,queryset,view):
        cid=request.query_params.get('cid')
        return queryset.filter(cid=cid)


class PageViewArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = "__all__"

class ArticleView(ListAPIView):   # 继承ListModelMixin,GenericAPIView
    authentication_classes = []      # 根据请求方法，同意添加约束属性失败，因为无法获取request.method方法
    permission_classes = []
    filter_backends = [FilterBackend,]
    queryset = models.Article.objects.all()
    serializer_class = [Show_article,]
class Add_Article(CreateAPIView):   # 两张表格进行序列化，关键是建立序列化的类，通过可能是通过连表查询将另一张表的字段添加到一个序列化类中,
    # 然后将数据提交后进行统一验证。  注意保存类与提交类之间的差异。
    # Article_serializer_class = [Save_article,]
    # Articledetails_serializer_class=[Articledetails,]
    serializer_class = Save_article  # 关键是要信息可以加入，同时校验成功jik.
    def perform_create(self, serializer):
        serializer.save()
class SingleAritcle(RetrieveAPIView,UpdateAPIView,DestroyAPIView,GenericAPIView):  # 注意此时查看单条评论不需要提供认证级登录，但是其他功能，
    # 例如更新与删除时需要作者才有权限去操作，所以需要认证，不能为空。此时需要加上方法判断条件
    # retrieve中内部会将路由上的pk值获取，而不用单独传参数，多余作废


    # def get(self,request,*args,**kwargs):
        # result=super().get(request,*args,**kwargs)
        # pk=kwargs.get('pk')
        # models.Article.objects.filter(pk=pk).update(read_count=F('read_count')+1)
        # return result

        # result=super().get(request,*args,**kwargs)
        # instance=self.get_object()   # 获取到当前对象，此时url中带有参数
        # print(instance)
        # instance.read_count+=1
        # instance.save()
        # return result
    queryset = models.Article.objects.all()
    # filter_backends = [SingleFilterBackend,]
    serializer_class = Save_article
    def get_authenticators(self):
        if self.request.method=="GET":
            authentication_classes = []
            permission_classes = []
# {"img":1,"category": 1,"status": 1,"author": "bbb","content": "bbb","title": "BBBB","create_at": "2019-11-09T04:11:47.551011Z","scan": 0,"comment_count":1}



class CommentView(CreateAPIView,UpdateAPIView,DestroyAPIView,RetrieveAPIView):
    serializer_class = PageViewArticleSerializer

    # def get_authenticators(self):
    #     if self.request.method == "GET":
    #         authors_id = self.request.query_params.get('authors_id')
    #         queryset = models.Comment.objects.filter(authors_id=authors_id)
    #         authentication_classes = []
    #         permission_classes = []
    #         serializer_class=[CommentSerializer,]
    #     elif self.request.method == "DELETE":
    #         authors_id = self.request.query_params.get('authors_id')
    #         queryset = models.Comment.objects.filter(authors_id=authors_id)
    #         filter_backends = [CommentFilterBackend, ]
    #
    #     else:
    #         authors_id = self.request.query_params.get('authors_id')
    #         filter_backends = [CommentFilterBackend, ]
    #         queryset = models.Comment.objects.filter(authors_id=authors_id)
    #         serializer_class = [Save_comment, ]

















# class ArticleView(APIView):
#     def get(self,request,*args,**kwargs):
#         pk=kwargs.get('pk')
#         if not pk:
#             # 通过将去的数据进行封装到字典，然后到筛选时，打散数据，用于查询。
#             # condition = {}
#             # category = request.query_params.get('category')
#             # if category:
#             #     condition['category'] = category
#             # queryset = models.Article.objects.filter(**condition).order_by('-date')
#
#             queryset = models.Article.objects.all()
#             page_object = PageNumberPagination()
#             result=page_object.paginate_queryset(queryset,request,self)
#             ser=Show_article(instance=result,many=True)
#         else:
#             queryset=models.Article.objects.filter(pk=pk).first()
#             ser=Show_article(instance=queryset,many=False)
#         return Response(ser.data)

# class CommentView(APIView):
    # authentication_classes = [Authentication,]
    # permission_classes = [Permission,]
    #
    # def get(self, request, *args, **kwargs):
    #     return Response('获取所有评论')
    #
    # def post(self,request,*args,**kwargs):
    #     if request.user:
    #         pass # 可以评论
    #     # 不可以评论
