from django.contrib import admin

# Register your models here.
from H1 import models
admin.site.register(models.Article)
admin.site.register(models.UserInfo)
admin.site.register(models.ArticleDetail)
admin.site.register(models.Comment)


# username: huolala
# password:huolala123