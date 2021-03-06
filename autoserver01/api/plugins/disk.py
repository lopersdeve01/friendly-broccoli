from api import models
from .base import BasePlugins

def process_disk(disk_info,server_object):
    new_disk_slot_set = set(disk_info.keys())
    # [obj,obj]
    db_disk_queryset = models.Disk.objects.filter(server=server_object)
    db_disk_dict = {obj.slot: obj for obj in db_disk_queryset}
    db_disk_slot_set = set(db_disk_dict.keys())

    record_msg_list = []

    # 新增的槽位集合
    create_slot_set = new_disk_slot_set - db_disk_slot_set
    create_object_list = []
    for slot in create_slot_set:
        # models.Disk.objects.create(**disk_info[slot],server=server_object)
        create_object_list.append(models.Disk(**disk_info[slot], server=server_object))
    if create_object_list:
        models.Disk.objects.bulk_create(create_object_list, batch_size=10)
        msg = "【新增硬盘】在%s槽位新增了硬盘。" % ",".join(create_slot_set)
        record_msg_list.append(msg)

    # 要删除的槽位集合
    remove_slot_set = db_disk_slot_set - new_disk_slot_set  # (1,2)
    models.Disk.objects.filter(server=server_object, slot__in=remove_slot_set).delete()
    if remove_slot_set:
        msg = "【删除硬盘】在%s槽位删除了硬盘。" % ",".join(remove_slot_set)
        record_msg_list.append(msg)

    # 要更新的槽位集合（可能有也可能没有）
    update_slot_set = new_disk_slot_set & db_disk_slot_set
    for slot in update_slot_set:
        temp = []
        row_dict = disk_info[
            slot]  # {'slot': '0', 'pd_type': 'SAS', 'capacity': '100', 'model': 'SEAGATE ST300MM0006     LS08S0K2B5NV'}
        row_object = db_disk_dict[
            slot]  # row_object.slot/ row_object.pd_type = getattr(row_object,'pd_type') / row.capacity /row.model
        for key, value in row_dict.items():
            if value != getattr(row_object, key):
                msg = "%s由%s变更为%s" % (key, getattr(row_object, key), value)
                temp.append(msg)
                setattr(row_object, key, value)
        if temp:
            slot_msg = "【更新硬盘】槽位%s:%s" % (slot, ",".join(temp))
            record_msg_list.append(slot_msg)
            row_object.save()

    if record_msg_list:
        models.Record.objects.create(server=server_object, content="\n".join(record_msg_list))


class Disk(BasePlugins):

    def process(self,disk,server_object):
        if not disk['status']:
            print('采集资产错误',disk['error'])
            return
        disk_info = disk['data']
        new_disk_slot_set = set(disk_info.keys())
        # [obj,obj]
        db_disk_queryset = models.Disk.objects.filter(server=server_object)
        db_disk_dict = {obj.slot: obj for obj in db_disk_queryset}
        db_disk_slot_set = set(db_disk_dict.keys())

        record_msg_list = []

        # 新增的槽位集合
        create_slot_set = new_disk_slot_set - db_disk_slot_set
        create_object_list = []
        for slot in create_slot_set:
            # models.Disk.objects.create(**disk_info[slot],server=server_object)
            create_object_list.append(models.Disk(**disk_info[slot], server=server_object))
        if create_object_list:
            models.Disk.objects.bulk_create(create_object_list, batch_size=10)
            msg = "【新增硬盘】在%s槽位新增了硬盘。" % ",".join(create_slot_set)
            record_msg_list.append(msg)

        # 要删除的槽位集合
        remove_slot_set = db_disk_slot_set - new_disk_slot_set  # (1,2)
        models.Disk.objects.filter(server=server_object, slot__in=remove_slot_set).delete()
        if remove_slot_set:
            msg = "【删除硬盘】在%s槽位删除了硬盘。" % ",".join(remove_slot_set)
            record_msg_list.append(msg)

        # 要更新的槽位集合（可能有也可能没有）
        update_slot_set = new_disk_slot_set & db_disk_slot_set
        for slot in update_slot_set:
            temp = []
            row_dict = disk_info[slot]  # {'slot': '0', 'pd_type': 'SAS', 'capacity': '100', 'model': 'SEAGATE ST300MM0006     LS08S0K2B5NV'}
            row_object = db_disk_dict[slot]  # row_object.slot/ row_object.pd_type = getattr(row_object,'pd_type') / row.capacity /row.model
            for key, value in row_dict.items():
                if value != getattr(row_object, key):
                    msg = "%s由%s变更为%s" % (key, getattr(row_object, key), value)
                    temp.append(msg)
                    setattr(row_object, key, value)
            if temp:
                slot_msg = "【更新硬盘】槽位%s:%s" % (slot, " ".join(temp))
                record_msg_list.append(slot_msg)
                row_object.save()

        if record_msg_list:
            models.Record.objects.create(server=server_object, content="\n".join(record_msg_list))
