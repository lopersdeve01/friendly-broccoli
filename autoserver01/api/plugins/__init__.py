import importlib
from django.conf import settings
def process_server_info(info,server_object):
    """
    处理中控汇报资产信息
    :return:
    """
    for key,path in settings.CMDB_PLUGIN_DICT.items():

        module_path,class_name = path.rsplit('.',maxsplit=1)
        module = importlib.import_module(module_path)
        instance = getattr(module,class_name)(key)

        instance.process(info[key],server_object)
