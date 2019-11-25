from django.db import models

# Create your models here.


class Server(models.Model):
    """ 服务器表 """
    status_choices = (
        (1,'上线'),
        (2,'下线'),
    )
    status = models.IntegerField(verbose_name='状态',choices=status_choices,default=1)
    hostname=models.CharField(verbose_name='IP地址',max_length=64)
    last_date = models.DateField(verbose_name='最新采集资产时间', null=True, blank=True)

class Memory(models.Model):
    slot=models.CharField(verbose_name='slot',max_length=32)
    capacity=models.CharField(verbose_name='capacity',max_length=32)
    model=models.CharField(verbose_name='model',max_length=255)
    speed=models.CharField(verbose_name='speed',max_length=32)
    manufacturer=models.CharField(verbose_name='manufacturer',max_length=255)
    sn=models.CharField(verbose_name='sn',max_length=255)
    server=models.ForeignKey('Server',verbose_name='ip')

class Disk(models.Model):
    """ 硬盘 """
    slot = models.CharField(verbose_name='槽位',max_length=32)
    pd_type = models.CharField(verbose_name='类型',max_length=255)
    capacity = models.CharField(verbose_name='容量',max_length=255)
    model = models.CharField(verbose_name='型号',max_length=255)
    server = models.ForeignKey(verbose_name='主机',to='Server')


class Record(models.Model):
    """ 资产更变记录 """
    server = models.ForeignKey(verbose_name='服务器',to='Server')
    content = models.TextField(verbose_name='变更内容')
    date = models.DateTimeField(verbose_name='时间',auto_now_add=True)

class Board(models.Model):
    manufacturer = models.CharField(verbose_name='制造商',max_length=32)
    sn = models.CharField(verbose_name='sn',max_length=255)
    model = models.CharField(verbose_name='型号',max_length=255)
    server = models.ForeignKey(verbose_name='主机',to='Server')

class Nic(models.Model):
    name = models.CharField(verbose_name='name', max_length=32)
    up = models.BooleanField(verbose_name='up')
    hwaddr = models.CharField(verbose_name='hwaddr', max_length=255)
    address= models.CharField(verbose_name='address', max_length=32)
    netmask= models.CharField(verbose_name='netmask', max_length=32)
    broadcast= models.CharField(verbose_name='broadcast', max_length=32)
    server = models.ForeignKey(verbose_name='主机', to='Server')


class CPU(models.Model):
    processor = models.CharField(verbose_name='处理器', max_length=32)
    cpu_family = models.CharField(verbose_name='cpu_family', max_length=255)
    cpu_cores = models.CharField(verbose_name='cpu_cores', max_length=255)
    cache_size = models.CharField(verbose_name='cache_size', max_length=255)
    clflush_size = models.CharField(verbose_name='clflush_size', max_length=255)
    model_name = models.CharField(verbose_name='model_name', max_length=255,default='aa')
    server = models.ForeignKey(verbose_name='主机', to='Server')

