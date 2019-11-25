from django.db import models

class Depart(models.Model):
    """ 部门表 """
    title = models.CharField(verbose_name='部门',max_length=32)


class Server(models.Model):
    """ 服务器表 """
    status_choices = (
        (1,'上线'),
        (2,'下线'),
    )
    status = models.IntegerField(verbose_name='状态',choices=status_choices,default=1)
    hostname = models.CharField(verbose_name='主机名',max_length=32)

    depart = models.ForeignKey(verbose_name='部门', to='Depart')

    last_date = models.DateField(verbose_name='最新采集资产时间',null=True,blank=True)

    # board
    sn = models.CharField(verbose_name='SN号',max_length=64,null=True,blank=True)
    model = models.CharField(verbose_name='SN号',max_length=64,null=True,blank=True)
    manufacturer = models.CharField(verbose_name='SN号',max_length=64,null=True,blank=True)

    # CPU
    cpu_count = models.IntegerField(verbose_name='CPU逻辑核数',null=True,blank=True)
    cpu_physical_count = models.IntegerField(verbose_name='CPU物理核数', null=True,blank=True)
    cpu_model = models.CharField(verbose_name='CPU型号',max_length=64,null=True,blank=True)


class Disk(models.Model):
    """ 硬盘 """
    slot = models.CharField(verbose_name='槽位',max_length=16)
    pd_type = models.CharField(verbose_name='类型',max_length=16)
    capacity = models.CharField(verbose_name='容量',max_length=16)
    model = models.CharField(verbose_name='型号',max_length=32)
    server = models.ForeignKey(verbose_name='主机',to='Server')


class Record(models.Model):
    """ 资产更变记录 """
    server = models.ForeignKey(verbose_name='服务器',to='Server')
    content = models.TextField(verbose_name='变更内容')
    date = models.DateTimeField(verbose_name='时间',auto_now_add=True)