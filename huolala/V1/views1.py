# 原处理方式，即序列化分页
# 关键引入类。序列化类 seriliazer以及

# 设置字段展示类（文章与评论），继承serializer.ModelSerializer
# 操作函数类,继承APIView

# 引入模块
from V1 import models
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Count,F

# 格式调整
from django.forms.models import model_to_dict



# 文章的增删改查
# 查询文章分为两部，一种整体查询，另一种单个查询
# 整体查询，需要拿到分类值，如果拿不到默认为全部，展示字段需要增加，自定制，优先采用method方式，单个展示与整体展示字段相同
# 增加文章，增加文章需要增加文章内容，即跨表增加，要求两个序列化与先后保存 ，文章字段定制，排除文章作者，详细内容排除文章id
# 编辑文章，类似类似增加文章，字段定制与增加文章相同
# 删除文章，基本上可以省略

# title = models.CharField(verbose_name='标题', max_length=32)
# # imgs = models.ForeignKey('Img',verbose_name='图片')
# category = models.IntegerField('文章分类', choices=category_choices, default=1)
# create_at = models.DateTimeField(auto_now_add=True, blank=True)
# status = models.IntegerField(verbose_name='状态', choices=status_choices, default=1)
# scan = models.IntegerField(verbose_name='阅读量', default=0)
# author = models.ForeignKey("User", verbose_name='作者')
# comment_count = models.IntegerField(verbose_name='评论数')


# content = models.TextField(verbose_name='评论内容', default=1)
# create_at = models.DateTimeField(auto_now_add=True, blank=True)
# users = models.ForeignKey('User', verbose_name='用户')
# articles = models.ForeignKey('Article', verbose_name='所属文章')




# 定制字段
# 展示字段
class Show_article(serializers.ModelSerializer):
    img=serializers.SerializerMethodField()
    category=serializers.CharField(source='get_category_display')
    status=serializers.SerializerMethodField()
    author=serializers.SerializerMethodField()
    content=serializers.SerializerMethodField()
    # comment_count=serializers.SerializerMethodField()
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
        exclude=['author']

class Articledetails(serializers.ModelSerializer):
    class Meta:
        model=models.ArticleDetails
        exclude=['articles']

class Show_comment(serializers.ModelSerializer):
    class Meta:
        model=models.Comment
        exclude=['articles']

class ArticleView(APIView):
    def get(self,request,*args,**kwargs):
        # pk=request.GET.get('pk')
        pk=kwargs.get('pk')
        # if not pk:
        #     ret = models.Article.objects.all()
        # else:
        #     ret= models.Article.objects.filter(pk=pk).first()
        # data={'ret':ret}
        # return Response(data)
        if not pk:
            queryset = models.Article.objects.all()
            ser=Show_article(instance=queryset,many=True)
        else:
            queryset=models.Article.objects.filter(pk=pk).first()
            ser=Show_article(instance=queryset,many=False)
        return Response(ser.data)



    # queryset = models.Category.objects.all().values_list('id', 'name')
    # data_list = list(queryset)
    # category_object = models.Category.objects.filter(id=pk).first()
    # data = model_to_dict(category_object)

    def patch(self,request,*args,**kwargs):
        category = request.GET.get('category')
        # ret = models.Article.objects.filter(category=category).first()
        # data = {'ret': ret}
        # return Response(data)
        queryset=models.Article.objects.filter(category=category).first()
        ser=Show_article(instance=queryset,many=True,partial=True)
        return Response(ser.data)
    def post(self,request,*args,**kwargs):
        author_id=kwargs.get('author_id')
        pk=kwargs.get('pk')
        # models.Article.objects.create(**request.data)
        # return Response('OK')
        ser_article=Save_article(data=request.data)
        ser_articledetail=Articledetails(data=request.data)
        if ser_article.is_valid() and ser_articledetail.is_valid():
            ser_article.save(author_id=author_id)
            ser_articledetail.save(articles_id=pk)
            return Response('添加成功')
        return Response('添加失败')
    def put(self,request,*args,**kwargs):
        pk=kwargs.get('pk')
        queryset = models.Article.objects.filter(pk=pk).first()
        ser = Show_article(data=request.data, instance=queryset)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)
    def delete(self,request,*args,**kwargs):
        pk=kwargs.get('pk')
        models.Article.objects.filter(pk=pk).delete()
        return Response('OK')
class CommentView(APIView):
    def post(self,request,*args,**kwargs):
        pk=kwargs.get('pk')
        ser=Show_comment(data=request.data)
        if ser.is_valid():
            ser.save(authors_id=pk)
            return Response(ser.data)
        return Response(ser.errors)
    def put(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        cid = kwargs.get('cid')
        queryset=models.Comment.objects.filter(cid=cid).first()
        ser = Show_comment(data=request.data,instance=queryset)
        if ser.is_valid():
            ser.save(authors_id=pk)
            return Response(ser.data)
        return Response(ser.errors)
    def delete(self,request,*args,**kwargs):
        cid=kwargs.get('cid')
        models.Comment.objects.filter(cid=cid).delete()
        return Response('OK')











# 评论的增删改查
# 评论查询在文章展示中出现，不再单独处理
# 评论增加  需要定制字段，排除文章id
# 评论编辑  需要定制字段，排除文章id
# 评论删除




