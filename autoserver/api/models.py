from django.db import models

# Create your models here.


class Host(models.Model):
    hostname=models.CharField(verbose_name='IP地址',max_length=64)

class Memory(models.Model):
    slot=models.CharField(verbose_name='slot',max_length=32)
    capacity=models.CharField(verbose_name='capacity',max_length=32)
    model=models.CharField(verbose_name='model',max_length=32)
    speed=models.CharField(verbose_name='speed',max_length=32)
    manufacturer=models.CharField(verbose_name='manufacturer',max_length=32)
    sn=models.CharField(verbose_name='sn',max_length=32)
    host=models.ForeignKey('Host',verbose_name='ip')



