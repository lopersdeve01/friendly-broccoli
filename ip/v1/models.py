from django.db import models

# Create your models here.

class Id(models.Model):
    name=models.CharField(max_length=32,verbose_name="IP地址")