import importlib
from django.conf import settings
def process_server_info(info,server_object):
    """
    处理中控汇报资产信息
    :return:
    """
    for key,path in settings.CMDB_PLUGIN_DICT.items():   # 将配置信息的字典里内容加以处理，拿到字典中的类模块，将类实例化，并将数据返回

        module_path,class_name = path.rsplit('.',maxsplit=1)
        # print('__init__class_name',class_name)
        module = importlib.import_module(module_path)
        instance = getattr(module,class_name)()   # 实例化类对象
        instance.process(info[key],server_object)  # 将参数封装进类中，进行处理
