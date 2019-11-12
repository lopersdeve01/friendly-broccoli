from django.contrib import admin

# Register your models here.
from insects import models


admin.site.register(models.UserInfo)
admin.site.register(models.Department)
admin.site.register(models.Customer)
admin.site.register(models.Campuses)
admin.site.register(models.ClassList)

# username:oldbeast
# password:olddog123