from api import models

class CPU(object):

    def process(self,cpu,server_object):     # 获取新的硬盘信息数据
        if not cpu['status']:
            print('采集资产错误',cpu['error'])  # 采集信息错误
            return
        cpu_info = cpu['data']
        print('autoserver_cpu_info',cpu_info)
        new_cpu_processor_set = set(cpu_info.keys())
        # [obj,obj]
        db_cpu_queryset = models.CPU.objects.filter(server=server_object)
        db_cpu_dict = {obj.processor: obj  for obj in db_cpu_queryset}
        db_cpu_processor_set = set(db_cpu_dict.keys())

        record_msg_list = []

        # 新增的槽位集合
        create_processor_set = new_cpu_processor_set - db_cpu_processor_set
        print('create_processor_set',create_processor_set)
        create_object_list = []
        for processor in create_processor_set:
            # models.CPU.objects.create(**cpu_info[processor],server=server_object)
            create_object_list.append(models.CPU(**cpu_info[processor], server=server_object))
        if create_object_list:
            models.CPU.objects.bulk_create(create_object_list, batch_size=10)
            msg = "【新增硬盘】在%s槽位新增了硬盘。" % ",".join(create_processor_set)
            record_msg_list.append(msg)

        # 要删除的槽位集合
        remove_processor_set = db_cpu_processor_set - new_cpu_processor_set  # (1,2)
        print('remove_processor_set',remove_processor_set)
        models.CPU.objects.filter(server=server_object, processor__in=remove_processor_set).delete()
        if remove_processor_set:
            msg = "【删除硬盘】在%s槽位删除了硬盘。" % ",".join(remove_processor_set)
            record_msg_list.append(msg)

        # 要更新的槽位集合（可能有也可能没有）
        update_processor_set = new_cpu_processor_set & db_cpu_processor_set
        print('update_processor_set',update_processor_set)
        for processor in update_processor_set:
            temp = []
            row_dict = cpu_info[processor]  # {'processor': '0', 'pd_type': 'SAS', 'capacity': '100', 'model': 'SEAGATE ST300MM0006     LS08S0K2B5NV'}
            row_object = db_cpu_dict[processor]  # row_object.processor/ row_object.pd_type = getattr(row_object,'pd_type') / row.capacity /row.model
            for key, value in row_dict.items():
                if value != getattr(row_object, key):
                    msg = "%s由%s变更为%s" % (key, getattr(row_object, key), value)
                    temp.append(msg)
                    setattr(row_object, key, value)
            if temp:
                processor_msg = "【更新硬盘】槽位%s:%s" % (processor, " ".join(temp))
                record_msg_list.append(processor_msg)
                row_object.save()

        if record_msg_list:
            models.Record.objects.create(server=server_object, content="\n".join(record_msg_list))