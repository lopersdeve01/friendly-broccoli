from api import models
#  此处的plugins中的py文件的功能是将获取服务器的信息进行加工筛选，并保存在数据库中，执行API的功能。
#  调用方法是从setting中将文件的路经与信息获取到，然后逐个解析执行，将数据保存在数据库中
def process_disk(disk_info,server_object):   #  instance.process(info[key],server_object)  disk_info 为新获取的硬盘字典信息，而后者为服务器的对象，前者的字典信息来自于该服务器
    new_disk_slot_set = set(disk_info.keys()) # 针对硬盘的槽位处理，来自与新采集的数据，集合中主要是新获取信息字典的键，
    # 也就是唯一标识，对于硬盘来讲应该是槽数
    # [obj,obj]
    db_disk_queryset = models.Disk.objects.filter(server=server_object)  #   来自与数据库的数据
    db_disk_dict = {obj.slot: obj for obj in db_disk_queryset}  # 将来自数据库的信息加工成字典，（字典的键为槽数，字典的值为model对象），再将字典加工成集合
    db_disk_slot_set = set(db_disk_dict.keys())   # 同样用于校对的数据库信息的集合只有唯一标识，字典的键——槽数 

    record_msg_list = []  # 新的处理信息集合

    # 新增的槽位集合  ）增加槽位信息采用新的槽位信息减去旧的槽位信息，二者采用差集
    create_slot_set = new_disk_slot_set - db_disk_slot_set
    create_object_list = []   # 将差异的对象，就是字典的的键
    for slot in create_slot_set:
        # models.Disk.objects.create(**disk_info[slot],server=server_object)  # disk_info,为新采集数据信息中的硬盘信息字典，server为服务器的对象或者服务器的pk
        create_object_list.append(models.Disk(**disk_info[slot], server=server_object))   # 新保存数据列表
    if create_object_list:
        models.Disk.objects.bulk_create(create_object_list, batch_size=10)   # 批量添加，后面的batch_size为批量添加一次处理的最大数量
        msg = "【新增硬盘】在%s槽位新增了硬盘。" % ",".join(create_slot_set)  # 信息保存为**号硬盘，新增硬盘或者槽位
        record_msg_list.append(msg)                             # 统一记录硬盘变更信息

    # 要删除的槽位集合
    remove_slot_set = db_disk_slot_set - new_disk_slot_set  # (1,2)  # 删除硬盘差集，不过是数据库的硬盘信息减去新获取的硬盘信息
    models.Disk.objects.filter(server=server_object, slot__in=remove_slot_set).delete() # 此次考察的就是批量删除，采用slot__in方法完成数剧的的筛选
    if remove_slot_set:
        msg = "【删除硬盘】在%s槽位删除了硬盘。" % ",".join(remove_slot_set)    # 信息保留情况同添加相同
        record_msg_list.append(msg)

    # 要更新的槽位集合（可能有也可能没有）     
    update_slot_set = new_disk_slot_set & db_disk_slot_set      # 更新槽位获取变更槽数信息较为容易，但是如何更新叫有难度，一种方法是筛选出变更信息，将
    # 将新获取的信息打散替换原有信息（set处理），另一种是一点一点将变更信息查出，并一一修改，此时会比较占用内存，但是相对而言，获取的信息较多。
    # 思路时一个一个信息在两类数据中进行比对，如果发现不同，用新的信息替换就有的信息，作为标记，同时加入到变更的详细记录中
    for slot in update_slot_set:
        temp = []
        row_dict = disk_info[
            slot]  # {'slot': '0', 'pd_type': 'SAS', 'capacity': '100', 'model': 'SEAGATE ST300MM0006     LS08S0K2B5NV'}  # 新的数据信息
        row_object = db_disk_dict[
            slot]  # row_object.slot/ row_object.pd_type = getattr(row_object,'pd_type') / row.capacity /row.model        # 旧的数据信息
        for key, value in row_dict.items():         #  如果新的数据信息，与旧的数据信息不同，
            if value != getattr(row_object, key):   # 获取对象属性，括号中前者为queryset对象（用. 加字段来获取值），后者为对象的属性名称（字段名称）
                msg = "%s由%s变更为%s" % (key, getattr(row_object, key), value)  #发现字段有差异，记录差异字段
                temp.append(msg)    # 保存修改信息
                setattr(row_object, key, value)  # 更改差异字段
        if temp:
            slot_msg = "【更新硬盘】槽位%s:%s" % (slot, ",".join(temp))
            record_msg_list.append(slot_msg)   
            row_object.save()     # 如果存在修改，将修改后的结果保存，如果没有修改，那么就不执行处理
  
    if record_msg_list:
        models.Record.objects.create(server=server_object, content="\n".join(record_msg_list))  # 将修改记录保存进数据库


class Disk(object):  

    def process(self,disk,server_object):     # 获取新的硬盘信息数据
        if not disk['status']:
            print('采集资产错误',disk['error'])  # 采集信息错误
            return
        disk_info = disk['data']
        print('autoserver_disk_info',disk_info)
        new_disk_slot_set = set(disk_info.keys())
        # [obj,obj]
        db_disk_queryset = models.Disk.objects.filter(server=server_object)
        db_disk_dict = {obj.slot: obj  for obj in db_disk_queryset}
        db_disk_slot_set = set(db_disk_dict.keys())

        record_msg_list = []

        # 新增的槽位集合
        create_slot_set = new_disk_slot_set - db_disk_slot_set
        print('create_slot_set',create_slot_set)
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
        print('remove_slot_set',remove_slot_set)
        models.Disk.objects.filter(server=server_object, slot__in=remove_slot_set).delete()
        if remove_slot_set:
            msg = "【删除硬盘】在%s槽位删除了硬盘。" % ",".join(remove_slot_set)
            record_msg_list.append(msg)

        # 要更新的槽位集合（可能有也可能没有）
        update_slot_set = new_disk_slot_set & db_disk_slot_set
        # print('update_slot_set',update_slot_set)
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

#getattr(object, name[,default])
#获取对象object的属性或者方法，如果存在打印出来，如果不存在，打印出默认值，默认值可选。
#需要注意的是，如果是返回的对象的方法，返回的是方法的内存地址，如果需要运行这个方法，
#可以在后面添加一对括号