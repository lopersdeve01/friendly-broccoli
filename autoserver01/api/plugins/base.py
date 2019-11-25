class BasePlugins(object):
    def __init__(self,key):
        self.key = key

    def process(self,info,server_object):
        raise NotImplementedError('子类必须实现process方法')