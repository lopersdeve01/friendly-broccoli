from api import models
from .base import BasePlugins

class Board(BasePlugins):
    def process(self, info, server_object):
        if not info['status']:
            print(info['error'])
            return
        cpu_info = info['data']
        record_msg = []
        for key,new_value in cpu_info.items():
            old_value = getattr(server_object,key)
            verbose_name = models.Server._meta.get_field(key).verbose_name
            if new_value != old_value:
                setattr(server_object,key,new_value)
                msg = "【更新主板】%s 由 %s 变更为%s " %(verbose_name,old_value,new_value)
                record_msg.append(msg)
        if record_msg:
            models.Record.objects.create(content="\n".join(record_msg),server=server_object)
            server_object.save()

