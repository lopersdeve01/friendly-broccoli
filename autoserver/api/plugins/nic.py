from api import models
class Nic(object):

    def process(self,nic,server_object):     # 获取新的硬盘信息数据
        if not nic['status']:
            print('采集资产错误',nic['error'])  # 采集信息错误
            return
        nic_info = nic['data']
        print('autoserver_nic_info',nic_info)
        new_nic_name_set = set(nic_info.keys())  # enss33
        # [obj,obj]
        db_nic_queryset = models.Nic.objects.filter(server=server_object)
        db_nic_dict = {obj.name:obj  for obj in db_nic_queryset}
        db_nic_name_set = set(db_nic_dict.keys())

        record_msg_list = []

        # 新增的槽位集合
        create_name_set = new_nic_name_set - db_nic_name_set
        print('create_name_set',create_name_set)
        create_object_list = []
        for name in create_name_set:
            # models.Nic.objects.create(**nic_info[name],server=server_object)
            data = dict(nic_info[name]['inet'][0])
            print(type(data))
            nic_info[name].pop('inet')
            print('nic_info[name]',nic_info[name])
            create_object_list.append(models.Nic(**nic_info[name],**data,name=name, server=server_object))
        if create_object_list:
            models.Nic.objects.bulk_create(create_object_list, batch_size=10)
            msg = "【新增硬盘】在%s槽位新增了硬盘。" % ",".join(create_name_set)
            record_msg_list.append(msg)

        # 要删除的槽位集合
        remove_name_set = db_nic_name_set - new_nic_name_set  # (1,2)
        print('remove_name_set',remove_name_set)
        models.Nic.objects.filter(server=server_object, name__in=remove_name_set).delete()
        if remove_name_set:
            msg = "【删除硬盘】在%s槽位删除了硬盘。" % ",".join(remove_name_set)
            record_msg_list.append(msg)

        # 要更新的槽位集合（可能有也可能没有）
        update_name_set = new_nic_name_set & db_nic_name_set
        print('update_name_set',update_name_set)
        for name in update_name_set:
            temp = []
            data=dict(nic_info[name]['inet'][0])
            nic_info[name].pop('inet')
            for k,v in data.items():
                nic_info[name].update(k=v)
            row_dict = nic_info[name].update(name=name) # {'name': '0', 'pd_type': 'SAS', 'capacity': '100', 'model': 'SEAGATE ST300MM0006     LS08S0K2B5NV'}
            row_object = db_nic_dict[name]  # row_object.name/ row_object.pd_type = getattr(row_object,'pd_type') / row.capacity /row.model
            for key, value in row_dict.items():
                if value != getattr(row_object, key):
                    msg = "%s由%s变更为%s" % (key, getattr(row_object, key), value)
                    temp.append(msg)
                    setattr(row_object, key, value)
            if temp:
                name_msg = "【更新硬盘】槽位%s:%s" % (name, " ".join(temp))
                record_msg_list.append(name_msg)
                row_object.save()

        if record_msg_list:
            models.Record.objects.create(server=server_object, content="\n".join(record_msg_list))