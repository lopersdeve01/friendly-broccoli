from api import models
class Board(object):

    def process(self,board,server_object):     # 获取新的硬盘信息数据
        if not board['status']:
            print('采集资产错误',board['error'])  # 采集信息错误
            return
        board_info = board['data']
        print('autoserver_board_info',board_info)
        # new_board_model_set = set(board_info)
        # print('new_board_model_set',new_board_model_set)
        # [obj,obj]
        db_board = models.Board.objects.filter(server=server_object)
        print("db_board",db_board)
        print(getattr(db_board,'model'))
        # db_board_dict = {obj.model: obj  for obj in db_board_queryset}
        # db_board_model_set = set(obj for obj in db_board_queryset)
        # print('db_board_model_set',db_board_model_set)

        # record_msg_list = []

        # 新增的槽位集合
        # create_model_set = new_board_model_set - db_board_model_set
        if board_info!=db_board:
            if board_info and db_board:
                temp = []
                for key, value in board_info.items():
                    if value != getattr(db_board, key):
                        msg = "%s由%s变更为%s" % (key, getattr(db_board, key), value)
                        temp.append(msg)
                        setattr(db_board, key, value)
                # if temp:
                #     model_msg = "【更新主板】槽位%s:%s" % (model, " ".join(temp))
                #     record_msg_list.append(model_msg)
                    db_board.save()
            elif len(board_info)==0:
                models.Board.objects.filter(model=board_info['model']).delete()

            else:
                models.Board.objects.create(**board_info,server=server_object)

            # print('create_model_set',create_model_set)
        # create_object_list = []
        # for model in create_model_set:
        #     # models.Board.objects.create(**board_info[model],server=server_object)
        #     create_object_list.append(models.Board(**board_info, server=server_object))
        # if create_object_list:
        #     models.Board.objects.bulk_create(create_object_list, batch_size=10)
        #     msg = "【新增硬盘】在%s槽位新增了硬盘。" % ",".join(create_model_set)
        #     record_msg_list.append(msg)
        #
        # # 要删除的槽位集合
        # remove_model_set = db_board_model_set - new_board_model_set  # (1,2)
        # print('remove_model_set',remove_model_set)
        # models.Board.objects.filter(server=server_object, model__in=remove_model_set).delete()
        # if remove_model_set:
        #     msg = "【删除硬盘】在%s槽位删除了硬盘。" % ",".join(remove_model_set)
        #     record_msg_list.append(msg)
        #
        # # 要更新的槽位集合（可能有也可能没有）
        # update_model_set = new_board_model_set & db_board_model_set
        # print('update_model_set',update_model_set)
        # for model in update_model_set:
        #     temp = []
        #     row_dict = board_info[model]  # {'model': '0', 'pd_type': 'SAS', 'capacity': '100', 'model': 'SEAGATE ST300MM0006     LS08S0K2B5NV'}
        #     row_object = db_board_dict[model]  # row_object.model/ row_object.pd_type = getattr(row_object,'pd_type') / row.capacity /row.model
        #     for key, value in row_dict.items():
        #         if value != getattr(row_object, key):
        #             msg = "%s由%s变更为%s" % (key, getattr(row_object, key), value)
        #             temp.append(msg)
        #             setattr(row_object, key, value)
        #     if temp:
        #         model_msg = "【更新硬盘】槽位%s:%s" % (model, " ".join(temp))
        #         record_msg_list.append(model_msg)
        #         row_object.save()

        # if record_msg_list:
        #     models.Record.objects.create(server=server_object, content="\n".join(record_msg_list))