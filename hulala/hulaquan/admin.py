from django.contrib import admin

# Register your models here.
from hulaquan import models

admin.site.register(models.Tag)
admin.site.register(models.Article)
admin.site.register(models.Comment)
admin.site.register(models.UserInfo)
