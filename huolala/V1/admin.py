from django.contrib import admin

# Register your models here.
from V1 import models

admin.site.register(models.Img)
admin.site.register(models.Article)
admin.site.register(models.Comment)
admin.site.register(models.ArticleDetails)
admin.site.register(models.User)
admin.site.register(models.Role)
admin.site.register(models.Permission)